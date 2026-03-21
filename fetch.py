import requests
import sqlite3
base_url = "https://api.open-meteo.com/v1/forecast"
parameters = {"daily": "temperature_2m_max,precipitation_sum,windspeed_10m_max", "timezone": "Europe/Copenhagen"}
def get_weather(lat, lon, location):
    params = parameters.copy()
    params["latitude"] = lat
    params["longitude"] = lon

    response = requests.get(base_url, params=params)
    data = response.json()
    
    return {"location": location, "date": data["daily"]["time"][1], "temperature": data["daily"]["temperature_2m_max"][1], "wind": data["daily"]["windspeed_10m_max"][1]}

def save_to_db(data):
    conn = sqlite3.connect("weather.db")
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS weather (location TEXT, date TEXT, temperature REAL, wind REAL, PRIMARY KEY (location, date)) """)
    for row in data:
        cursor.execute(""" INSERT OR REPLACE INTO weather (location, date, temperature, wind) VALUES (?, ?, ?, ?)""", (row["location"], row["date"], row["temperature"], row["wind"]))
    conn.commit()
    conn.close()

def main():
    locations = [("Hua Hin", 12.5684, 99.9577), ("Bangkok", 13.7563, 100.5018), ("Aalborg", 57.0488, 9.9217)]
    results = []
    for name, lat, lon in locations:
        weather = get_weather(lat, lon, name)
        results.append(weather)
    
    for r in results: print(r)
    save_to_db(results)

if __name__ == "__main__":
    main()