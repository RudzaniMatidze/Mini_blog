""" Routes script handles the different URLs that the application supports"""
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
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