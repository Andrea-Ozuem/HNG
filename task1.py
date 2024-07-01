#!/usr/bin/python3
'''a script that starts a Flask web application'''

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
IP_KEY = os.getenv('IP_KEY')

@app.route('/api/hello', methods=['GET'], strict_slashes=False)
def index():
    '''Return simple response'''
    name = request.args.get('visitor_name')
    if request.headers.getlist("X-Forwarded-For"):
        user_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        user_ip = request.remote_addr

    # get city
    url = f'https://ip-geolocation.whoisxmlapi.com/api/v1?apiKey={IP_KEY}&ipAddress={user_ip}'
    geoip_data = requests.get(url).json()
    city = geoip_data['location']['region']

    # get weather information
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    weather_res = requests.get(weather_url).json()
    temp = weather_res['main']['temp']

    greeting = f'Hello, {name}!, the temperature is {temp} degrees Celsius in {city}'
    response = {
      "client_ip": user_ip,
      "location": city,
      "greeting": greeting
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
