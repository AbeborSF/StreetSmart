from flask import render_template
from app import app

@app.route('/crime_insights')
def crime_insights():
    return render_template('crime_insights.html')