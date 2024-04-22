"""
These are presets for creating our databases. 
Models are used for creating classes that we'll use repeatedly to populate our databases.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#UUID stands for universally unique identifiers. 
#These are great for creating independent items that won't clash with other items
import uuid 

#imports date and time
from datetime import datetime, timedelta


#Werkzeug is a security package. This allows us to make the password data that we store in our 
#database secret, so that if we log in to look at our database, 
#we can't see what users saved as their password!
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets


# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # default_duration=db.Column(db.Integer,nullable=True)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Cycle(db.Model):
    id = db.Column(db.String, primary_key = True)
    last_period_date = db.Column(db.Date, nullable=False)
    period_duration = db.Column(db.Integer, nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,last_period_date,period_duration,user_token, id = ''):
        print("starting init")
        self.id = self.set_id()
        self.last_period_date = last_period_date
        self.period_duration = period_duration
        self.user_token = user_token
        print("ending init")


    def __repr__(self):
        return f'The following data has been added to the library: {self.last_period_date} by {self.period_duration}'

    def set_id(self):
        return (secrets.token_urlsafe())

class CycleSchema(ma.Schema):
    class Meta:
        fields = ['id', 'last_period_date','period_duration']

cycle_schema = CycleSchema()
cycles_schema = CycleSchema(many=True)