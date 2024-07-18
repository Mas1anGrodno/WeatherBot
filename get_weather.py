import requests, json
from deep_translator import GoogleTranslator

# Enter your API key here
api_key = "3efb07367c44620fb67d99e607fca049"


def get_weather(city_name, country_name):

    # тут получаем координаты по названию города                                               🠗🠗🠗 - limit=1 ограничивает количество совпадений названия города
    coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_name}&limit=1&appid={api_key}"
    get_coord = requests.get(coord_by_name)
    coord = get_coord.json()
    lat = coord[0]["lat"]
    lon = coord[0]["lon"]

    # получаем погоду по координатам
    weather_request = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily,minutely&units=metric&lang=ru&appid={api_key}"
    response = requests.get(weather_request)
    x = response.json()

    y = x["current"]
    z = y["weather"]

    city_name_from_json = coord[0]["name"]
    weather_description = z[0]["description"]
    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]

    # Пока отключили overview и вынесли в отдельную функцию.

    # overview_url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&units=metric&lang=ru&appid={api_key}"
    # overview = requests.get(overview_url)
    # j = overview.json()
    # weather_overview = j["weather_overview"]
    # translated = GoogleTranslator(source="en", target="ru").translate(weather_overview)

    # return f" В {city_name_from_json} сейчас - {weather_description}\nТемпература воздуха - {current_temperature} °C\nДавление - {current_pressure} гПа\nВлажность - {current_humidity} % \n\n{translated}"
    return f" В {city_name_from_json} сейчас - {weather_description}\nТемпература воздуха - {current_temperature} °C\nДавление - {current_pressure} гПа\nВлажность - {current_humidity} %"


def get_weather_overview(city_name, country_name):

    coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_name}&limit=1&appid={api_key}"
    get_coord = requests.get(coord_by_name)
    coord = get_coord.json()
    lat = coord[0]["lat"]
    lon = coord[0]["lon"]

    overview_url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&units=metric&lang=ru&appid={api_key}"
    overview = requests.get(overview_url)
    j = overview.json()

    weather_overview = j["weather_overview"]
    city_name_from_json = coord[0]["name"]

    translated = GoogleTranslator(source="en", target="ru").translate(weather_overview)

    return f" В {city_name_from_json} сейчас -\n{translated}"
