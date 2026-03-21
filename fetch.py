import requests
import sqlite3


#API
base_url = "https://api.open-meteo.com/v1/forecast"
parameters = {"daily": "temperature_2m_max,precipitation_sum,windspeed_10m_max", "timezone": "Europe/Copenhagen"}

#FETCH WEATHER
def get_weather(lat, lon, location):
    params = parameters.copy()
    params["latitude"] = lat
    params["longitude"] = lon

    response = requests.get(base_url, params=params)
    data = response.json()
    
    return {"location": location, "date": data["daily"]["time"][1], "temperature": data["daily"]["temperature_2m_max"][1], "wind": data["daily"]["windspeed_10m_max"][1]}

#SAVE TO DATABASE
def save_to_db(data):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS weather (location TEXT, date TEXT, temperature REAL, wind REAL, PRIMARY KEY (location, date)) """)
    for row in data:
        cursor.execute(""" INSERT OR REPLACE INTO weather (location, date, temperature, wind) VALUES (?, ?, ?, ?)""", (row["location"], row["date"], row["temperature"], row["wind"]))
    conn.commit()
    conn.close()
