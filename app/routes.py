""" Routes script handles the different URLs that the application supports"""

from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import logout_user, login_required, current_user, login_user
from datetime import datetime, timezone
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
import sqlalchemy as sa
from app import app, db

# Create an index route
@app.route('/')
@app.route('/index')
@login_required
def index():
    # Create a Mock objects used to test application
    user = { 'username': 'Rudzani'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Johannesburg!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Coding is so interesting!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

# Create a login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login view function logic
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

# Create logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Create a Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Registration view function logic
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congradulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Create a user profile route
@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# Create edit user profile route
@app.route('/edit_profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                            form=form)

# Record time of last visit
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()