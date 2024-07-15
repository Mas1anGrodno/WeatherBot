# import required modules
import requests, json

# Enter your API key here
api_key = "3efb07367c44620fb67d99e607fca049"

# base_url variable to store url
# base_url = "http://api.openweathermap.org/data/2.5/weather?"
# base_url = "https://api.openweathermap.org/data/3.0/onecall?lat=53.6884&lon=23.8258&appid=api_key"
res = requests.get("http://api.openweathermap.org/data/2.5/weather", params={"id": city_id, "units": "metric", "lang": "ru", "APPID": appid})
# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":
    print(x)
    # store the value of "main"
    # key in variable y
    y = x["current"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature = y["temp"]

    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidity = y["humidity"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]

    # print following values
    print(
        " Temperature (in kelvin unit) = "
        + str(current_temperature)
        + "\n atmospheric pressure (in hPa unit) = "
        + str(current_pressure)
        + "\n humidity (in percentage) = "
        + str(current_humidity)
        + "\n description = "
        + str(weather_description)
    )

else:
    print(" City Not Found ")
