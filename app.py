#!flask/bin/python


from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests
import json
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

class Posts(UserMixin, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), nullable=False)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/userHome')
def userHome():
    return render_template('userHome.html')

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

@app.route('/displayposts')
def displayposts():
    posts = Posts.query.all()

    for post in posts:
        text = post.text

    return render_template('displayposts.html', posts=posts)

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    post = Posts(text=text)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('displayposts'))


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
        return redirect(url_for('firstTime'))
    login_user(user, True)
    return redirect(url_for('userHome'))



@app.route('/map')

def mapview():
    send_url = "http://freegeoip.net/json"
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    position = [lat, lon]

    targetX = 37.363835099999996,
    targetY = -120.42992299999999,

    tutorTotal = 6 #hardcoded
    markers = []

# creating a map in the 
    sndmap = Map(
        zoom_control = True,
        scale_control = True,
        zoom = 9,
        identifier="sndmap",
        lat= float(position[0]),
        lng= float(position[1]),


        markers=[
        {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat':position[0],
            'lng': position[1],
            'infobox': "<b>My Location</b>" +"<br>" + str(position[0]) + " , " + str(position[1])
        },
        {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            'lat': targetX,
            'lng': targetY,
            'infobox': "<b>Tutor</b>" +"<br>" + str(targetX) + " , " + str(targetY)
        }
        ]
        )	
    return render_template('mapTest.html', sndmap = sndmap)
 

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
    db.create_all()
    app.run(debug=True)
