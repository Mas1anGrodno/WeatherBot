import requests

from deep_translator import GoogleTranslator
from datetime import datetime, timezone

from .weather_requests import get_weather_forecast, get_weather_forecast_overview


def convert_unix_timestamp_to_hours(unix_timestamp: int, time_offset: int) -> str:
    unix_timestamp += time_offset
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).strftime("%H:%M:")


def convert_unix_timestamp_to_days(unix_timestamp: int, time_offset: int) -> str:
    unix_timestamp += time_offset
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).strftime("%d-%m-%Y")


def weather_now(city_name: str = None, country_name: str = None, lat: float = None, lon: float = None) -> str:
    print(city_name, country_name)
    try:
        weather_data = get_weather_forecast(city_name, country_name, lat, lon)
        if not weather_data:
            raise ValueError("Данные не получены")

        current_time = convert_unix_timestamp_to_hours(weather_data["current"]["dt"], weather_data["timezone_offset"])
        weather_description = weather_data["current"]["weather"][0]["description"]

        sunrise = convert_unix_timestamp_to_hours(weather_data["daily"][0]["sunrise"], weather_data["timezone_offset"])
        sunset = convert_unix_timestamp_to_hours(weather_data["daily"][0]["sunset"], weather_data["timezone_offset"])
        current_temp = round(weather_data["current"]["temp"])
        feels_like_temp = round(weather_data["current"]["feels_like"])
        # current_pressure = weather_data["current"]["pressure"]
        # current_humidity = weather_data["current"]["humidity"]
        temp_min = round(weather_data["daily"][0]["temp"]["min"])
        temp_max = round(weather_data["daily"][0]["temp"]["max"])
        temp_night = round(weather_data["daily"][0]["temp"]["night"])
        temp_feels_morn = round(weather_data["daily"][0]["feels_like"]["morn"])
        temp_feels_day = round(weather_data["daily"][0]["feels_like"]["day"])
        temp_feels_eve = round(weather_data["daily"][0]["feels_like"]["eve"])

        pressure = weather_data["daily"][0]["pressure"]
        humidity = weather_data["daily"][0]["humidity"]

        if "alerts" in weather_data and weather_data["alerts"]:
            weather_alerts_start = convert_unix_timestamp_to_hours(weather_data["alerts"][0]["start"], weather_data["timezone_offset"])
            weather_alerts_end = convert_unix_timestamp_to_hours(weather_data["alerts"][0]["end"], weather_data["timezone_offset"])
            weather_alerts = GoogleTranslator(source="en", target="ru").translate(weather_data["alerts"][0]["event"])
        else:
            weather_alerts_start = None
            weather_alerts_end = None
            weather_alerts = None

        alerts_info = ""

        if weather_alerts_start and weather_alerts_end:
            alerts_info = f"⚠️ C {weather_alerts_start} до {weather_alerts_end} возможны(ен): {weather_alerts}"

        return f"""
📅 Сейчас: {current_time}

🌅 Восход: {sunrise}
🌄 Закат: {sunset}

🌆 В выбранной локации сейчас: {weather_description}

🌡 Температура воздуха: {current_temp} °C
🤗 Ощущается как: {feels_like_temp} °C
🌡 Днем от {temp_min} до {temp_max} °C
  ощущается как
    Утром: {temp_feels_morn} °C
    Днем: {temp_feels_day} °C
    Вечером: {temp_feels_eve} °C
🌡 Ночью: {temp_night} °C
🌬 Давление: {pressure} гПа
💧 Влажность: {humidity} %

{alerts_info}
"""

    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# Вызов с названием города и кодом страны
# print(weather_now(city_name="Grodno", country_name="BY"))


# Вызов с координатами
# print(weather_now(lat=53.6884, lon=23.8258))


def weather_hourly(city_name: str = None, country_name: str = None, lat: float = None, lon: float = None) -> str:
    forecast = []
    try:
        weather_data = get_weather_forecast(city_name, country_name, lat, lon)
        if not weather_data:
            raise ValueError("Данные не получены")

        for i in range(1, 10, 2):
            time = convert_unix_timestamp_to_hours(weather_data["hourly"][i]["dt"], weather_data["timezone_offset"])
            temp = round(weather_data["hourly"][i]["temp"])
            weather_description = weather_data["hourly"][i]["weather"][0]["description"]
            forecast.append(f"🕑: {time} 🌡 : {temp} 🌥 : {weather_description}")

        return "\n".join(forecast)

    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# Вызов с названием города и кодом страны
# print(weather_hourly(city_name="Grodno", country_name="BY"))

# Вызов с координатами
# print(weather_hourly(lat=53.6884, lon=23.8258))


def weather_three_days(city_name: str = None, country_name: str = None, lat: float = None, lon: float = None) -> str:
    forecast = []
    try:
        weather_data = get_weather_forecast(city_name, country_name, lat, lon)
        if not weather_data:
            raise ValueError("Данные не получены")

        for i in range(1, 4):
            current_time = convert_unix_timestamp_to_days(weather_data["daily"][i]["dt"], weather_data["timezone_offset"])
            summary = GoogleTranslator(source="en", target="ru").translate(weather_data["daily"][i]["summary"])

            sunrise = convert_unix_timestamp_to_hours(weather_data["daily"][i]["sunrise"], weather_data["timezone_offset"])
            sunset = convert_unix_timestamp_to_hours(weather_data["daily"][i]["sunset"], weather_data["timezone_offset"])

            temp_min = round(weather_data["daily"][i]["temp"]["min"])
            temp_max = round(weather_data["daily"][i]["temp"]["max"])
            temp_night = round(weather_data["daily"][i]["temp"]["night"])
            temp_feels_morn = round(weather_data["daily"][i]["feels_like"]["morn"])
            temp_feels_day = round(weather_data["daily"][i]["feels_like"]["day"])
            temp_feels_eve = round(weather_data["daily"][i]["feels_like"]["eve"])

            pressure = weather_data["daily"][i]["pressure"]
            humidity = weather_data["daily"][i]["humidity"]
            # icon = weather_data["daily"][i]["weather"][i]["icon"]
            # URL иконки
            # icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

            forecast.append(
                f"""
                📅 {current_time} - {summary}
                🌅 Восход:{sunrise}
                🌄 Закат:{sunset}
                🌡 Днем от {temp_min} до {temp_max} °C
                Ощущается как
                Утром: {temp_feels_morn} °C
                Днем: {temp_feels_day} °C
                Вечером: {temp_feels_eve} °C
                🌡 Ночью: {temp_night} °C
                🌬 Давление: {pressure} гПа
                💧 Влажность: {humidity} %
                """
            )
        return "\n".join(forecast)

    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# Вызов с названием города и кодом страны
# print(weather_three_days(city_name="Grodno", country_name="BY"))

# Вызов с координатами
# print(weather_three_days(lat=53.6884, lon=23.8258))


def weather_overview(city_name: str = None, country_name: str = None, lat: float = None, lon: float = None) -> str:
    try:
        weather_data_overview = get_weather_forecast_overview(city_name, country_name, lat, lon)
        if not weather_data_overview:
            raise ValueError("Данные описания погодных условий не получены")

        translated_overview = GoogleTranslator(source="en", target="ru").translate(weather_data_overview["weather_overview"])
        return translated_overview
    except (requests.RequestException, ValueError) as e:
        return f"Ошибка: {e}"


# Вызов с названием города и кодом страны
# print(weather_overview(city_name="Grodno", country_name="BY"))

# Вызов с координатами
# print(weather_overview(lat=53.6884, lon=23.8258))
