from app.forms import UserLoginForm
from app.models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import jsonify

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Get JSON data from the request

    email = data.get('email')
    password = data.get('password')

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    # Create a new user
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    print(email, password)

    return jsonify({'message': 'User created successfully'}), 201


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successful in your initiation. Congratulations, and welcome to the Jedi Knights', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('You do not have access to this content.', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))