import requests
from datetime import datetime

API_KEY = "7d3929a308b385e4e4dd44d314687940"


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")


def extract_weather_data(data):
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "visibility": round(data.get("visibility", 0) / 1000, 1),
        "wind": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "sunrise": format_time(data["sys"]["sunrise"]),
        "sunset": format_time(data["sys"]["sunset"])
    }


def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("Error:", response.text)
            return None

        data = response.json()

        return extract_weather_data(data)

    except Exception as e:
        print("Weather Error:", e)
        return None


def get_weather_by_coordinates(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print("Error:", response.text)
            return None

        data = response.json()

        return extract_weather_data(data)

    except Exception as e:
        print("Coordinate Error:", e)
        return None


if __name__ == "__main__":
    print("\nTesting Weather API\n")

    city = input("Enter city name: ")

    weather = get_weather(city)

    if weather:
        print("\nWeather Data:")
        print(weather)
    else:
        print("\nFailed to fetch weather data.")