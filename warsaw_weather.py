import requests
from APIkey import api_key


def get_current_weather():
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q=Warsaw&aqi=no"

    r = requests.get(url)
    weather = r.json()["current"]
    return (
        weather["temp_c"],
        weather["feelslike_c"],
        weather["precip_mm"],
        weather["cloud"],
        weather["humidity"],
        weather["pressure_mb"],
        weather["condition"]["text"],
        weather["last_updated"],
    )
