from flask import render_template, url_for, redirect
from covid_app import app, db


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')
