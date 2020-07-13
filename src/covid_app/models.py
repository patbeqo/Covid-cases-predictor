from covid_app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cityName = db.Column(db.String, unique=True)
    longitude = db.Column(db.String)
    lattitude = db.Column(db.String)
    currNum = db.Column(db.String)
    foreNum = db.Column(db.String)

    def __repr__(self):
        return f"City('{self.cityName}', '{self.longitude}', '{self.lattitude}', '{self.currNum}', '{self.foreNum}')"