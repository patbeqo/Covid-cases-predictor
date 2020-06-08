from flask import Flask, render_template, url_for
import folium


app = Flask(__name__)



posts = [
    {
        'author': 'Patrik',
        'title': 'Testing Title',
        'content': 'Testing content',
        'date_posted': 'April 20,2018'
    },
    {
        'author': 'Beqo',
        'title': 'second Title',
        'content': 'second content',
        'date_posted': 'March 20,2018'
    }
]

@app.route('/')
@app.route('/home')
def home():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    folium_map.save('templates/map.html')
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)