from deep_translator import GoogleTranslator
from datetime import datetime, timezone
from weather_requests import get_city_coord, weather_request, weather_request_overview


def convert_unix_timestamp(unix_timestamp: int) -> str:
    weather_data = weather_request(coords)
    offset = weather_data["timezone_offset"]
    unix_timestamp += offset
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).strftime("%H:%M:")


coords = get_city_coord("grodno", "by")


def weather_now():
    weather_data = weather_request(coords)

    current_time = convert_unix_timestamp(weather_data["current"]["dt"])
    current_temp = weather_data["current"]["temp"]
    feels_like = weather_data["current"]["feels_like"]
    current_pressure = weather_data["current"]["pressure"]
    current_humidity = weather_data["current"]["humidity"]
    weather_description = weather_data["current"]["weather"][0]["description"]

    return f"""
    Сейчас - {current_time}
    В выбранной локации сейчас - {weather_description}
    Температура воздуха - {current_temp} °C
    Ощущается как - {feels_like} °C
    Давление - {current_pressure} гПа
    Влажность - {current_humidity} %
    """


# print(weather_now())


def weather_now_plus_three_hours():
    weather_data = weather_request(coords)
    current_time = convert_unix_timestamp(weather_data["current"]["dt"])
    current_temp = weather_data["current"]["temp"]
    weather_description = weather_data["current"]["weather"][0]["description"]

    time_plus_3 = convert_unix_timestamp(weather_data["hourly"][3]["dt"])
    time_plus_3_temp = weather_data["hourly"][3]["temp"]
    time_plus_3_weather_description = weather_data["hourly"][3]["weather"][0]["description"]

    time_plus_6 = convert_unix_timestamp(weather_data["hourly"][6]["dt"])
    time_plus_6_temp = weather_data["hourly"][6]["temp"]
    time_plus_6_weather_description = weather_data["hourly"][6]["weather"][0]["description"]

    time_plus_9 = convert_unix_timestamp(weather_data["hourly"][9]["dt"])
    time_plus_9_temp = weather_data["hourly"][9]["temp"]
    time_plus_9_weather_description = weather_data["hourly"][9]["weather"][0]["description"]

    return f"""
    Сейчас - {current_time}
    Температура воздуха {current_temp} °C и {weather_description}

    в - {time_plus_3}
    Температура воздуха {time_plus_3_temp} °C и {time_plus_3_weather_description}

    в - {time_plus_6}
    Температура воздуха {time_plus_6_temp} °C и {time_plus_6_weather_description}

    в - {time_plus_9}
    Температура воздуха {current_temp} °C и {weather_description}
    """


# print(weather_now_plus_three_hours())


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


print(weather_today())

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


def overview():
    weather_data_overview = weather_request_overview(coords)

    translated_overview = GoogleTranslator(source="en", target="ru").translate(weather_data_overview["weather_overview"])
    print(translated_overview)


# overview()
