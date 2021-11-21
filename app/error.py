from flask import render_template
from app import app


@app.errorhandler(404)
def not_found_error(error):
    # If the application has a 404 error
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # If the application has an internal error
    return render_template('500.html'), 500
