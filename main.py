from fetch import get_weather, save_to_db
from generate import generate_poem, save_poem
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