#used to create the Flask application
from flask import Flask, render_template

#Myconfig  contains configuration settings for the Flask app, such as database details.
from config import Myconfig

"""
These lines below import blueprints from different parts of the application. 
Blueprints are a way to organize a group of related views and other code. 
It imports api, site, and auth blueprints 
which are likely to handle API endpoints, site-related routes, and authentication routes

"""
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth

#Importing SQLAlchemy, an Object-Relational Mapping (ORM) tool 
#allows you to interact with databases using Python classes.
from flask_sqlalchemy import SQLAlchemy



from flask_migrate import Migrate
from app.models import db as root_db, login_manager, ma

#The CORS is to avoid Cross-Site Request Forgery, or CSRF. 
from flask_cors import CORS


#custom class from Flask to convert data to json format when jsonify() is used or when
#json response directly returned from flask routes
from app.helpers import JSONEncoder


#importing Flask and the code below creates an instance of app
app = Flask(__name__)
CORS(app)
print("Hello World")


#now app registers the below blueprints
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)


app.json_encoder = JSONEncoder

# These lines initiate the database within the app
#and run login manager. Also get app ready and modify using Migrate
app.config.from_object(Myconfig)
print(Myconfig.__dict__)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)
