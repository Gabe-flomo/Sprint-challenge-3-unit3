"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq_py as openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {}>'.format(self.datetime,self.value)

def get_data():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles',parameter='pm25')
    results = body['results']
    return results


def add_data(results):
    DB.drop_all()
    DB.create_all()
    
    for result in results:
        #print(result['date']['utc'],result['value'])
        data = Record(datetime=result['date']['utc'],value=result['value'])
        DB.session.add(data)

    DB.session.commit()  


@APP.route('/')
def root():
    """Base view."""
    '''api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles',parameter='pm25')
    results = body['results'][:2]
    time_value = []
    for result in results:
        time_value.append(str((result['date']['utc'],result['value'])))
    '''
    #data = get_data()
    #add_data(data)
    filtered = Record.query.filter(Record.value > 10).all()
    
    return str(filtered)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'