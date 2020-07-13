from flask import render_template, url_for, redirect
from covid_app import app, db
from covid_app.models import City

import folium

from selenium import webdriver
from bs4 import BeautifulSoup




@app.route('/')
@app.route('/home')
def home():
    
    ############ The code below creates and customizes the map ################

    # Creates map object starting in New York City with Styling applied
    m = folium.Map(width='75%', height='50%', left='12.5%', location=[40.7128, -74.0060], zoom_start=5)

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