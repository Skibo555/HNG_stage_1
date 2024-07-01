from flask import Flask, jsonify, request
import requests
import os

# Instantiating
app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to the home page!</h1><p style='color: coral;'>Have a work around</p>"


@app.route("/api/hello")
def task_route():
    api_key = "b82801fd933a4a0aaf78ef1d82048722"
    weather_api_key = "cde973399f35f9cad81df7b715a40a45"
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    visitor_name = request.args.get('visitor_name', default="Anonymous")
    location_getter_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}"
    loc = requests.get(location_getter_url).json()
    ip_addr = loc["ip"]
    location = loc["city"]
    latitude = loc["latitude"]
    longitude = loc["longitude"]
    headers = {
        "lat": latitude,
        "lon": longitude,
        "appid": weather_api_key
    }

    weather_resp = requests.get(url=weather_url, params=headers).json()
    temperature = round(int(weather_resp["main"]["temp"]) - 273.15)
    resp_msg = {
        "client_ip": f"{ip_addr}",
        "location": f"{location}",
        "greeting": "Hello {}!, the temperature is {} degrees Celsius in {}".format(visitor_name, temperature, location)
    }
    return jsonify({"Response": resp_msg})


if __name__ == "__main__":
    app.run(debug=True)
