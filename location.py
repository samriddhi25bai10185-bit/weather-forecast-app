import requests

def get_location():
    try:
        response = requests.get(
            "http://ip-api.com/json/",
            timeout=10
        )

        data = response.json()

        return {
            "city": data.get("city"),
            "lat": data.get("lat"),
            "lon": data.get("lon")
        }

    except Exception:
        return None