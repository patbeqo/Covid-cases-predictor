#handles algorithm for machine learning
import csv
from covid_app import db
from covid_app.models import City

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

    with open('./static/covidData/usData.csv', mode='r') as csvfile: 
        data= list(csv.reader(csvfile))

        for i in range(56):
            cityData = []
            if data[(i+1)][1] != "AS" and data[(i+1)][1] != "GU" and data[(i+1)][1] != "MP" and data[(i+1)][1] != "VI":
                for j in range(10):
                    cityData.append(data[(i+1)+j*56])
                cityArray.append(cityData)

    print(cityArray)
    for i in range(52):
        myCity = City.query.filter_by(cityName=citydict[cityArray[i][1]]).first()
        myCity.currNum = cityArray[i][0]
        myCity.foreNum = getFutureCases(cityArray[i])

    #db.session.commit()
            
    def getFutureCases(cityData):
        #run regression model on data and predict future value
        print()