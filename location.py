import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from weather_api import get_weather, get_weather_by_coordinates
from location import get_location

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Weather Forecast Dashboard")
app.geometry("750x800")
app.resizable(False, False)

current_lat = None
current_lon = None

def get_weather_icon(condition):
    condition = condition.lower()

    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunder" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition:
        return "🌫️"

    return "🌤️"

def update_time():
    now = datetime.now()

    date_label.configure(
        text=now.strftime("%A, %d %B %Y")
    )

    time_label.configure(
        text=now.strftime("%I:%M:%S %p")
    )

    app.after(1000, update_time)

def update_weather(weather):
    weather_icon.configure(
        text=get_weather_icon(weather["condition"])
    )

    city_label.configure(
        text=weather["city"]
    )

    temp_label.configure(
        text=f"{round(weather['temperature'])}°C"
    )

    condition_label.configure(
        text=weather["condition"]
    )

    humidity_value.configure(
        text=f"{weather['humidity']}%"
    )

    wind_value.configure(
        text=f"{weather['wind']} m/s"
    )

def search_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror(
            "Error",
            "Please enter a city name."
        )
        return

    weather = get_weather(city)

    if weather is None:
        messagebox.showerror(
            "Error",
            "City not found."
        )
        return

    update_weather(weather)

def load_current_location_weather():
    global current_lat, current_lon

    location = get_location()

    if location is None:
        location_text.configure(
            text="📍 Location Not Detected"
        )
        return

    current_lat = location["lat"]
    current_lon = location["lon"]

    weather = get_weather_by_coordinates(
        current_lat,
        current_lon
    )

    if weather:
        location_text.configure(
            text=f"📍 Current Location: {weather['city']}"
        )

        city_entry.delete(0, "end")
        city_entry.insert(0, weather["city"])

        update_weather(weather)


def refresh_weather():
    if current_lat is None:
        return

    weather = get_weather_by_coordinates(
        current_lat,
        current_lon
    )

    if weather:
        update_weather(weather)


title_label = ctk.CTkLabel(
    app,
    text="Weather Forecast Dashboard",
    font=("Arial", 36, "bold")
)
title_label.pack(pady=(20, 10))

date_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 18)
)
date_label.pack()

time_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 24, "bold")
)
time_label.pack(pady=(0, 15))

location_text = ctk.CTkLabel(
    app,
    text="📍 Detecting Location...",
    font=("Arial", 18)
)
location_text.pack(pady=10)

search_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
search_frame.pack(pady=15)

city_entry = ctk.CTkEntry(
    search_frame,
    width=350,
    height=45,
    placeholder_text="Enter city name"
)
city_entry.grid(row=0, column=0, padx=10)

search_button = ctk.CTkButton(
    search_frame,
    text="Search",
    width=120,
    height=45,
    command=search_weather
)
search_button.grid(row=0, column=1)

weather_card = ctk.CTkFrame(
    app,
    width=600,
    height=300,
    corner_radius=25
)
weather_card.pack(pady=20)

weather_icon = ctk.CTkLabel(
    weather_card,
    text="🌤️",
    font=("Arial", 80)
)
weather_icon.pack(pady=(20, 5))

temp_label = ctk.CTkLabel(
    weather_card,
    text="--°C",
    font=("Arial", 60, "bold")
)
temp_label.pack()

city_label = ctk.CTkLabel(
    weather_card,
    text="City",
    font=("Arial", 28, "bold")
)
city_label.pack()

condition_label = ctk.CTkLabel(
    weather_card,
    text="Condition",
    font=("Arial", 20)
)
condition_label.pack(pady=(0, 20))

details_frame = ctk.CTkFrame(
    app,
    width=600,
    height=140,
    corner_radius=25
)
details_frame.pack(pady=15)

humidity_title = ctk.CTkLabel(
    details_frame,
    text="Humidity",
    font=("Arial", 20, "bold")
)
humidity_title.grid(row=0, column=0, padx=80, pady=(20, 5))

wind_title = ctk.CTkLabel(
    details_frame,
    text="Wind Speed",
    font=("Arial", 20, "bold")
)
wind_title.grid(row=0, column=1, padx=80, pady=(20, 5))

humidity_value = ctk.CTkLabel(
    details_frame,
    text="--",
    font=("Arial", 28)
)
humidity_value.grid(row=1, column=0, pady=10)

wind_value = ctk.CTkLabel(
    details_frame,
    text="--",
    font=("Arial", 28)
)
wind_value.grid(row=1, column=1, pady=10)

refresh_button = ctk.CTkButton(
    app,
    text="🔄 Refresh Current Location Weather",
    width=300,
    height=45,
    command=refresh_weather
)
refresh_button.pack(pady=20)

update_time()
load_current_location_weather()

app.mainloop()