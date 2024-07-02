from flask import Flask, jsonify, request
import requests
import os


"""
As much as there are not so much things here to explain, I just wish I play around with some comment.

Happy reviewing!
"""

# Instantiating my flask APP
app = Flask(__name__)


# Getting API KEY From the environment for security reasons
api_key = "b82801fd933a4a0aaf78ef1d82048722"
weather_api_key = "cde973399f35f9cad81df7b715a40a45"


# The home route, the marker may want to visit home and index some things, LOL
@app.route('/')
def home():
    # print(request.headers['X-Real-IP'])
    # ip = request.headers['X-Real-IP']
    user_agent = requests.get(f'https://api.ipgeolocation.io/user-agent?apiKey={api_key}')
    print(user_agent.json()["userAgentString"])
    return f"<h1>Welcome to the home page!<br> Your Ip is  </h1><p style='color: coral;'>Have a work around</p>"


# The take route, the actual endpoint
@app.route("/api/hello")
def task_route():

    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    # I set the default visitor to anonymous just in case the visitor does not provide their name.
    visitor_name = request.args.get('visitor_name', default="Anonymous")
    ip = request.headers['X-Real-IP']
    location_getter_url = f"https://ipapi.co/{ip}/json/"
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
    """The temperature from Weather API is in Kelvin so I had to convert it, the code below converts it to Celsius.
    and rounds it up.
    The response from the API too was in string so I need to convert it to an int to I can perform mathematical 
    operation on it.
    
    formular for converting kelvin to celsius is : celsius - 273.15.
    
    I hope any python developer that reads this will understand the code.
    """
    temperature = round(int(weather_resp["main"]["temp"]) - 273.15)
    resp_msg = {
        "client_ip": f"{ip_addr}",
        "greeting": "Hello {}!, the temperature is {} degrees Celsius in {}".format(visitor_name, temperature, location),
        "location": f"{location}"
    }
    return jsonify(resp_msg)


if __name__ == "__main__":
    app.run(debug=True)
