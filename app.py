import json
import urllib
import requests
from flask import Flask, render_template, url_for, flash, redirect, request
import logging

app = Flask(__name__)

messages = []


@app.route('/', methods=('GET', 'POST'))
def home_page():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        if not latitude:
            return 'Latitude is required!'
        elif not longitude:
            return 'Longitude is required!'
        else:
            messages.append({'latitude': latitude, 'longitude': longitude})
            return redirect(url_for('get_weather', lat=latitude, lon=longitude))

    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def get_weather():
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return 'Latitude and Longitude should be valid numbers!'

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&timezone=auto&forecast_days=3"


    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return render_template('weather.html', data=weather_data)
    else:
        return f"Failed to fetch weather data. Status code: {response.status_code}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
