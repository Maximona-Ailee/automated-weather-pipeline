import requests
import sqlite3
from groq import Groq
import os

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

#GROQ GENERATE POEM
def generate_poem(data):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f""" First imagine, you're little girl from Thailand and love to write poem, create the poem about comparing weather forcast tomorrow from these three locations:
    {data[0]['location']}: {data[0]['temperature']}°C, wind {data[0]['wind']}
    {data[1]['location']}: {data[1]['temperature']}°C, wind {data[1]['wind']}
    {data[2]['location']}: {data[2]['temperature']}°C, wind {data[2]['wind']}
    requirements:
    - compare the weather
    - suggest the nices place to be, and short about activity should be doing or foods should be eating in order to that place and weather
    - write in TWO languages: English and Thai
    - keep it short and creative
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages =[{"role": "user", "content": prompt}],
        temperature=1)

    return response.choices[0].message.content

#SAVE POEM
def save_poem(poem):
    with open("poem.txt", "w", encoding="utf-8") as f:
        f.write(poem)

#MAIN
def main():
    locations = [("Hua Hin", 12.5684, 99.9577), ("Bangkok", 13.7563, 100.5018), ("Aalborg", 57.0488, 9.9217)]
    results = []
    for name, lat, lon in locations:
        weather = get_weather(lat, lon, name)
        results.append(weather)
    
    for r in results: print(r)
    save_to_db(results)
    poem = generate_poem(results)
    print("POEM")
    print(poem)
    save_poem(poem)

if __name__ == "__main__":
    main()