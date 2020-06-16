from flask import render_template, url_for, redirect
from covid_app import app, db
import folium




@app.route('/')
@app.route('/home')
def home():
    
    ############ The code below creates and customizes the map ################

    # Creates map object starting in New York City with Styling applied
    m = folium.Map(width='75%', height='50%', left='12.5%', location=[40.7128, -74.0060], zoom_start=5)

    # Add marker for every capital city (Set to 10 just to test)
    for i in range(10):

        # Data will be grabbed from db
        cityName = 'helloworkd'
        currentCases = 'r'
        projectedCases = '32'
        longitude = 42.659829
        latitude = -73.781339

        # Popup message that will be displayed when user selects city
        msg='<p>Current: {currentCases}</p><p>Projected: {projectedCases}'.format(currentCases=currentCases, projectedCases=projectedCases)
        popup = folium.Popup(msg, max_width=2650)

        # Creates a marker ( + i for testing)
        folium.Marker([longitude + i, latitude + i], popup=popup, tooltip=cityName).add_to(m)

    # Creates the HTML file in order to display
    m.save('covid_app/templates/map.html')


    return render_template('home.html')
