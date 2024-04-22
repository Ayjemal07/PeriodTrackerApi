
#improrting os allows you to interface with the CLI and tell it commands
#(if you don't do it, flask will ask many direct questions)
import os


"""
Now we need to create a .env file (pronounced 'dot env', 
which is why the import calls on it). 
We're also joining the base directory (this is the line where we create the basedir variable)
and the .env file (the load_dotenv command takes care of this)
"""

from dotenv import load_dotenv,find_dotenv
basedir = os.path.abspath(os.path.dirname(__name__))
# load_dotenv(os.path.join(basedir, '.env'))
load_dotenv(find_dotenv())


class Myconfig():
    '''
        Set config variables for the flask app
        Using Environment variables where available.
        Otherwise create the config variable if not done already
    '''

    x=1
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    #commands to connect SQLAlchemy to the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_NOTIFICAITONS = False
