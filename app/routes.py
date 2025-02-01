""" Routes script handles the different URLs that the application supports"""

from flask import render_template, flash, redirect, url_for
from urllib.parse import urlsplit
from app.forms import LoginForm
from app.models import User
from sqlalchemy import sa
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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)

# create logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))