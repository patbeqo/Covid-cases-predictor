from flask import render_template, url_for, redirect
from covid_app import app, db
from covid_app.models import City

import folium
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup


def updateCases():
    citydict = {
        "AK" : "Alaska",
        "AL" : "Alabama",
        "AR" : "Arkansas",
        "AZ" : "Arizona",
        "CA" : "California",
        "CO" : "Colorado",
        "CT" : "Connecticut",
        "DC" : "District of Columbia",
        "DE" : "Delaware",
        "FL" : "Florida",
        "GA" : "Georgia",
        "HI" : "Hawaii",
        "IA" : "Iowa",
        "ID" : "Idaho",
        "IL" : "Illinois",
        "IN" : "Indiana",
        "KS" : "Kansas",
        "KY" : "Kentucky",
        "LA" : "Louisiana",
        "MA" : "Massachusetts",
        "MD" : "Maryland",
        "ME" : "Maine",
        "MI" : "Michigan",
        "MN" : "Minnesota",
        "MO" : "Missouri",
        "MS" : "Mississippi",
        "MT" : "Montana",
        "NC" : "North Carolina",
        "ND" : "North Dakota",
        "NE" : "Nebraska",
        "NH" : "New Hampshire",
        "NJ" : "New Jersey",
        "NM" : "New Mexico",
        "NV" : "Nevada",
        "NY" : "New York",
        "OH" : "Ohio",
        "OK" : "Oklahoma",
        "OR" : "Oregon",
        "PA" : "Pennsylvania",
        "PR" : "Puerto Rico",
        "RI" : "Rhode Island",
        "SC" : "South Carolina",
        "SD" : "South Dakota",
        "TN" : "Tennessee",
        "TX" : "Texas",
        "UT" : "Utah",
        "VA" : "Virginia",
        "VT" : "Vermont",
        "WA" : "Washington",
        "WI" : "Wisconsin",
        "WV" : "West Virginia",
        "WY" : "Wyoming"
    }

    cityArray = []

    with open('./covid_app/static/covidData/usData.csv', mode='r') as csvfile: 
        data= list(csv.reader(csvfile))

        for i in range(56):
            cityData = []
            if data[(i+1)][1] != "AS" and data[(i+1)][1] != "GU" and data[(i+1)][1] != "MP" and data[(i+1)][1] != "VI":
                for j in range(10):
                    cityData.insert(0, data[(i+1)+j*56])
                cityArray.append(cityData)

    for i in range(52):
        myCity = City.query.filter_by(cityName=citydict[cityArray[i][0][1]]).first()
        myCity.currNum = cityArray[i][9][2]
        myCity.foreNum = getFutureCases(i, cityArray)

    db.session.commit()

def getFutureCases(a, cityData):
    #run regression model on data and predict future value
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    X = [0,1,2,3,4,5,6,7,8,9]
    y = []
    for k in range(10):
        y.append(int(cityData[a][k][2]))

    df = pd.DataFrame(
        {'X': X,
        'y': y}
    )
    print(y)
    xmean = np.mean(X)
    ymean = np.mean(y)

    # Calculate the terms needed for the numator and denominator of beta
    df['xycov'] = (df['X'] - xmean) * (df['y'] - ymean)
    df['xvar'] = (df['X'] - xmean)**2

    # Calculate beta and alpha
    beta = df['xycov'].sum() / df['xvar'].sum()
    alpha = ymean - (beta * xmean)

    return int (alpha + beta * 10)

@app.route('/')
@app.route('/home')
def home():
    
    ############ The code below creates and customizes the map ################

    # Creates map object starting in New York City with Styling applied
    m = folium.Map(width='75%', height='50%', left='12.5%', location=[40.7128, -74.0060], zoom_start=5)

    #Updates cases data
    updateCases()

    # Database query for all City objects in database
    stateData = City.query.all()

    # Add marker for every US state
    for element in stateData:

        cityName = element.cityName
        currentCases = element.currNum
        projectedCases = element.foreNum
        longitude = element.longitude
        lattitude = element.lattitude

        # Popup message that will be displayed when user selects city
        msg='<p>Current: {currentCases}</p><p>Projected: {projectedCases}'.format(currentCases=currentCases, projectedCases=projectedCases)
        popup = folium.Popup(msg, max_width=2650)

        # Creates a marker ( + i for testing)
        folium.Marker([longitude, lattitude], popup=popup, tooltip=cityName).add_to(m)

    # Creates the HTML file in order to display
    m.save('covid_app/templates/map.html')

    return render_template('home.html')


# Web Scrape for US state names, longitude and lattitude
# Used to jumpstart project
# Only call if need to reset databse
def getCityNamesCoordinates():

    # Deletes entire databse
    db.drop_all()

    # Creates new database
    db.create_all()

    # Initialize new array store every states name, longitude and latitude
    states_array = []

    # Location of chromedriver.exe on my personal computer from where I run this program
    chromedriver = '/mnt/c/Program Files/chromedriver.exe'

    # Below fixes issues with the dynamic webpage replacing HTML content
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    browser= webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    # Website to scrape from
    url = "https://developers.google.com/public-data/docs/canonical/states_csv"

    # Grabs HTML from Website in order to parse
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, 'html.parser')

    data = soup.find(class_="devsite-table-wrapper").find_all("td")
    counter = 1
    tmp_arr = []

    for element in data:
        wantedText = element.get_text()
        if counter == 4:
            tmp_arr.insert(2, wantedText)
            states_array.insert(len(states_array), tmp_arr)
            tmp_arr = []
            counter = 1
        else:
            tmp_arr.insert(len(tmp_arr), wantedText)
            counter += 1
    
    # Takes data and stores in database
    for element in states_array:
        newCity = City(cityName=str(element[2]), longitude=str(element[1]), lattitude=str(element[3]), currNum='0', foreNum='0')
        db.session.add(newCity)
    
    db.session.commit()


    