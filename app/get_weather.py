import requests

from deep_translator import GoogleTranslator
from datetime import datetime, timezone

from .weather_requests import get_weather_forecast, weather_request, get_weather_forecast_overview


def convert_unix_timestamp(unix_timestamp: int) -> str:
    unix_timestamp += 10800
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).strftime("%H:%M:")


# coords = get_city_coord("grodno", "by")


def weather_now(city_name: str, country_name: str) -> dict:
    try:
        weather_data = get_weather_forecast(city_name, country_name)
        if not weather_data:
            raise ValueError("Данные не получены")

        print("Данные получены")
        current_time = convert_unix_timestamp(weather_data["current"]["dt"])
        weather_description = weather_data["current"]["weather"][0]["description"]

        current_temp = round(weather_data["current"]["temp"])
        feels_like_temp = round(weather_data["current"]["feels_like"])
        current_pressure = weather_data["current"]["pressure"]
        current_humidity = weather_data["current"]["humidity"]

        weather_alerts_start = convert_unix_timestamp(weather_data["alerts"][0]["start"])
        weather_alerts_end = convert_unix_timestamp(weather_data["alerts"][0]["end"])
        weather_alerts = GoogleTranslator(source="en", target="ru").translate(weather_data["alerts"][0]["event"])

        return f"""
Сейчас                              {current_time}                   
В выбранной локации сейчас          {weather_description}            
Температура воздуха                 {current_temp} °C                
Ощущается как                       {feels_like_temp} °C             
Давление                            {current_pressure} гПа           
Влажность                           {current_humidity} %             
C {weather_alerts_start} до {weather_alerts_end} возможны(ен) {weather_alerts} 
        """
    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# print(weather_now("grodno", "by"))


def weather_now_plus_three_hours(city_name: str, country_name: str) -> dict:

    try:
        weather_data = get_weather_forecast(city_name, country_name)
        if not weather_data:
            raise ValueError("Данные не получены")

        print("Данные получены")

        current_time = convert_unix_timestamp(weather_data["current"]["dt"])
        current_temp = round(weather_data["current"]["temp"])
        weather_description = weather_data["current"]["weather"][0]["description"]

        time_plus_3 = convert_unix_timestamp(weather_data["hourly"][3]["dt"])
        time_plus_3_temp = round(weather_data["hourly"][3]["temp"])
        time_plus_3_weather_description = weather_data["hourly"][3]["weather"][0]["description"]

        time_plus_6 = convert_unix_timestamp(weather_data["hourly"][6]["dt"])
        time_plus_6_temp = round(weather_data["hourly"][6]["temp"])
        time_plus_6_weather_description = weather_data["hourly"][6]["weather"][0]["description"]

        time_plus_9 = convert_unix_timestamp(weather_data["hourly"][9]["dt"])
        time_plus_9_temp = round(weather_data["hourly"][9]["temp"])
        time_plus_9_weather_description = weather_data["hourly"][9]["weather"][0]["description"]

        return f"""
        Сейчас - {current_time}
        Температура воздуха {current_temp} °C и {weather_description}

        в - {time_plus_3}
        Температура воздуха {time_plus_3_temp} °C и {time_plus_3_weather_description}

        в - {time_plus_6}
        Температура воздуха {time_plus_6_temp} °C и {time_plus_6_weather_description}

        в - {time_plus_9}
        Температура воздуха {time_plus_9_temp} °C и {time_plus_9_weather_description}
        """
    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# print(weather_now_plus_three_hours("grodno", "by"))


def weather_today():
    weather_data = weather_request(coords)

    current_temp = weather_data["current"]["temp"]
    feels_like = weather_data["current"]["feels_like"]
    current_pressure = weather_data["current"]["pressure"]
    current_humidity = weather_data["current"]["humidity"]
    weather_description = weather_data["current"]["weather"][0]["description"]

    return f"""
    Сегодня - {current_time}
    В выбранной локации сейчас - {weather_description}
    Температура воздуха - {current_temp} °C
    Ощущается как - {feels_like} °C
    Давление - {current_pressure} гПа
    Влажность - {current_humidity} %
    """


# print(weather_today())

# def weather_three_days():
#     weather_data = weather_request(coords)

#     time_plus_1_day = convert_unix_timestamp(weather_data["hourly"][3]["dt"])
#     time_plus_3_temp = weather_data["hourly"][3]["temp"]
#     time_plus_3_weather_description = weather_data["hourly"][3]["weather"][0]["description"]

#     time_plus_6 = convert_unix_timestamp(weather_data["hourly"][6]["dt"])
#     time_plus_6_temp = weather_data["hourly"][6]["temp"]
#     time_plus_6_weather_description = weather_data["hourly"][6]["weather"][0]["description"]

#     time_plus_9 = convert_unix_timestamp(weather_data["hourly"][9]["dt"])
#     time_plus_9_temp = weather_data["hourly"][9]["temp"]
#     time_plus_9_weather_description = weather_data["hourly"][9]["weather"][0]["description"]

#     return f"""
#     Сейчас - {current_time}
#     Температура воздуха {current_temp} °C и {weather_description}

#     в - {time_plus_3}
#     Температура воздуха {time_plus_3_temp} °C и {time_plus_3_weather_description}

#     в - {time_plus_6}
#     Температура воздуха {time_plus_6_temp} °C и {time_plus_6_weather_description}

#     в - {time_plus_9}
#     Температура воздуха {current_temp} °C и {weather_description}
#     """


# print(weather_three_days())


def weather_overview(city_name: str, country_name: str) -> dict:
    try:
        weather_data_overview = get_weather_forecast_overview(city_name, country_name)
        if not weather_data_overview:
            raise ValueError("Данные описания погодных условий не получены")

        translated_overview = GoogleTranslator(source="en", target="ru").translate(weather_data_overview["weather_overview"])
        return translated_overview
    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# print(weather_overview("grodno", "by"))
