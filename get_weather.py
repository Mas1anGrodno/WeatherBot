import requests, json

# Enter your API key here
api_key = "3efb07367c44620fb67d99e607fca049"

city_name = input("Enter city name : ")

coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},BY&limit=1&appid={api_key}"
get_coord = requests.get(coord_by_name)
coord = get_coord.json()
lat = coord[0]["lat"]
lon = coord[0]["lon"]
city_name_from_json = coord[0]["name"]

base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily,minutely&units=metric&lang=ru&appid={api_key}"
overview_url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&units=metric&lang=ru&appid={api_key}"

response = requests.get(base_url)
x = response.json()
overview = requests.get(overview_url)
j = overview.json()

y = x["current"]
z = y["weather"]


current_temperature = y["temp"]
current_pressure = y["pressure"]
current_humidity = y["humidity"]
weather_description = z[0]["description"]
weather_overview = j["weather_overview"]

print("Temperature (in celsius unit) = " + str(current_temperature))
print("Description = " + str(weather_description))
print("Humidity (in percentage) = " + str(current_humidity))
print("Atmospheric pressure (in hPa unit) = " + str(current_pressure))
print(weather_overview)
