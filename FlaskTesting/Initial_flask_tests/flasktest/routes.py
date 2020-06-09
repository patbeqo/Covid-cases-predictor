from flask import render_template, url_for, redirect
from flasktest import app
from flasktest.models import User


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
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')
