from typing import Tuple
import requests
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env(env_file=Path("./env/.env.dev"))

OW_API_KEY = env("OW_API_KEY")


def get_city_coord(city_name: str, country_name: str) -> Tuple[float, float]:
    coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_name}&limit=1&appid={OW_API_KEY}"
    get_coord = requests.get(coord_by_name)
    coord = get_coord.json()
    return float(coord[0]["lat"]), float(coord[0]["lon"])


def weather_request(coords: Tuple[float, float]) -> dict:
    lat, lon = coords
    weather_request = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&lang=ru&appid={OW_API_KEY}"
    r = requests.get(weather_request)
    response = r.json()
    return response


def weather_request_overview(coords: Tuple[float, float]) -> dict:
    lat, lon = coords
    weather_request_overview = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&units=metric&lang=ru&appid={OW_API_KEY}"
    r = requests.get(weather_request_overview)
    response = r.json()
    return response
