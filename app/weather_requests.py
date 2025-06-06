from typing import Tuple
import requests
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env(env_file=Path("./env/.env.dev"))

OW_API_KEY = env("OW_API_KEY")


def get_city_coord(city_name: str, country_name: str) -> Tuple[float, float]:
    coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_name}&limit=1&appid={OW_API_KEY}"
    try:
        get_coord = requests.get(coord_by_name)
        get_coord.raise_for_status()  # Проверка, что запрос выполнен успешно
        coord = get_coord.json()
        if not coord:
            raise ValueError("Данные координат не получены")
        return float(coord[0]["lat"]), float(coord[0]["lon"])
    except (requests.RequestException, ValueError) as e:
        print(f"Ошибка: {e}")
        return None, None


def weather_request(coords: Tuple[float, float]) -> dict:
    lat, lon = coords
    weather_request = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&lang=ru&appid={OW_API_KEY}"

    try:
        r = requests.get(weather_request)
        r.raise_for_status()  # Проверка, что запрос выполнен успешно
        response = r.json()
        if not response:
            raise ValueError("Данные о погоде не получены")
        return response
    except (requests.RequestException, ValueError) as e:
        print(f"Ошибка: {e}")
        return {}


def weather_request_overview(coords: Tuple[float, float]) -> dict:
    lat, lon = coords
    weather_request_overview = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&units=metric&lang=ru&appid={OW_API_KEY}"

    try:
        r = requests.get(weather_request_overview)
        r.raise_for_status()  # Проверка, что запрос выполнен успешно
        response = r.json()
        if not response:
            raise ValueError("Данные описаня погодных условий не получены")
        return response
    except (requests.RequestException, ValueError) as e:
        print(f"Ошибка: {e}")
        return {}


def get_weather_forecast(city_name: str = None, country_name: str = None, lat: float = None, lon: float = None) -> dict:
    # Проверяем, указаны ли координаты
    if lat is not None and lon is not None:
        coords = (lat, lon)
    elif city_name is not None and country_name is not None:
        # Получаем координаты города, если координаты не указаны
        coords = get_city_coord(city_name, country_name)
        if coords == (None, None):
            print("Ошибка: не удалось получить координаты города.")
            return {}
        # print(f"Координаты получены: {coords}")  # Отладочный вывод
    else:
        print("Ошибка: необходимо указать либо координаты, либо название города и код страны.")
        return {}

    # Получаем данные прогноза погоды по координатам
    weather_data = weather_request(coords)
    if weather_data:
        return weather_data
    else:
        print("Данные о погоде не получены или пустые")
        return {}


def get_weather_forecast_overview(city_name: str = None, country_name: str = None, lat: float = None, lon: float = None) -> dict:
    # Проверяем, указаны ли координаты
    if lat is not None and lon is not None:
        coords = (lat, lon)
    elif city_name is not None and country_name is not None:
        # Получаем координаты города, если координаты не указаны
        coords = get_city_coord(city_name, country_name)
        if coords == (None, None):
            print("Ошибка: не удалось получить координаты города.")
            return {}

    # Затем получаем данные прогноза погоды по координатам
    weather_data = weather_request_overview(coords)
    if weather_data:
        return weather_data
    else:
        print("Данные о погоде не получены или пустые")
        return {}
