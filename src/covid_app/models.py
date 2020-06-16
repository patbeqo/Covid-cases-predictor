from covid_app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String, unique=True)
    current_number = db.Column(db.Integer)
    forecasted_number = db.Column(db.Integer)