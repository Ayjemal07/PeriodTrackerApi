from flask import Blueprint, render_template

"""
Importting Blueprint helps in a way that when we run the app, 
we actually instantiate these objects - in this case, they're functions and the templates. 
The Blueprint import allows us to use the templates and access the file structure around them.
"""

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')