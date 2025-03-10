""" Script for error handling"""
from flask import render_template
from app import app, db

# Error handling for 404(not found)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Error handling for 500(internal error)
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500