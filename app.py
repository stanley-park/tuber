#!flask/bin/python

from flask import Flask, redirect, url_for, render_template, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests
import json
import pygeoip
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt




app = Flask(__name__)
app.config['SECRET_KEY'] = '24242424'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '408792279458709',
        'secret': '046aa45aec64338848b150b4713f2b04'
    }
}
app.config['GOOGLEMAPS_KEY'] = "AIzaSyCZUODD2xlOWl6lb14VwG24F3n8lh2gRoI"
GoogleMaps(app)

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    available = db.Column(db.Boolean, default=False)
    pending = db.Column(db.Integer, nullable=False, default=0)
    lat = db.Column(db.FLOAT, nullable=True)
    lon = db.Column(db.FLOAT, nullable=True)


class Posts(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    id_of_recipient = db.Column(db.Integer, nullable=False)

db.create_all()
db.session.commit()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')

@app.route('/pending', methods=['GET', 'POST'])
def pending():
    posts = Posts.query.all()

    return render_template('pending.html', posts=posts)

@app.route('/api/ip/<ip_address>')
def ip(ip_address):  
    geo_data = geolocate.record_by_addr(ip_address)
    return jsonify(geo_data)

@app.errorhandler(500)
def error_500(e):  
    return jsonify({'error': 'Error finding location data for that address'})


@app.route('/requestTutors')
def showRequestTutors():
    return render_template('requestTutors.html')

@app.route('/activateTutor')
def activateTutor():
    user = load_user(current_user.get_id())
    user.available = True
    db.session.commit()
    return redirect(url_for('userHome'))

@app.route('/deactivateTutor')
def deactivateTutor():
    user = load_user(current_user.get_id())
    user.available = False
    user.pending = 0

    posts = Posts.query.all()

    for indPost in posts:
        if (indPost.id_of_recipient == current_user.id):
            db.session.delete(indPost)
            

    db.session.commit()
    return redirect(url_for('userHome'))


@app.route('/signin.html')
def signIn():
    return render_template('signin.html')

@app.route('/makePost')
def makePost():
    return render_template('makePost.html')


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.route('/firstTime')
def showFirstTime():
    return render_template('firsttime.html')

@app.route('/displayposts', methods=['POST'])
def displayposts():
    users = User.query.all()

    return render_template('displayposts.html', users=users)

@app.route('/contact/<id>')
def contact(id):
    user = load_user(id)

    counter = 1

    post = Posts(id_of_recipient = id)

    posts = Posts.query.all()
    for indPost in posts:
        if (indPost.id_of_recipient == current_user.id):
            counter += 1



    db.session.add(post)

    user.pending = counter
    db.session.commit()
    return redirect(url_for('userHome'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('userHome'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('userHome'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('showFirstTime'))
    login_user(user, True)
    return redirect(url_for('userHome'))
 

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

    

if __name__ == '__main__':
    app.run(debug=True)
