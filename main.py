import customtkinter as ctk
from tkinter import messagebox
from weather_api import get_weather, get_weather_by_coordinates
from location import get_location

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Window
app = ctk.CTk()
app.title("Weather Forecast")
app.geometry("500x600")
app.resizable(False, False)


def update_weather_labels(weather):
    temperature_label.configure(
        text=f"🌡 Temperature: {weather['temperature']}°C"
    )

    humidity_label.configure(
        text=f"💧 Humidity: {weather['humidity']}%"
    )

    wind_label.configure(
        text=f"🌬 Wind Speed: {weather['wind']} m/s"
    )

    condition_label.configure(
        text=f"☁ Condition: {weather['condition']}"
    )


def search_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror(
            "Error",
            "Please enter a city name"
        )
        return

    weather = get_weather(city)

    if weather is None:
        messagebox.showerror(
            "Error",
            "City not found"
        )
        return

    update_weather_labels(weather)


def load_current_location_weather():
    location = get_location()

    if location is None:
        location_label.configure(
            text="📍 Location Not Detected"
        )
        return

    city = location["city"]
    lat = location["lat"]
    lon = location["lon"]

    location_label.configure(
        text=f"📍 Current Location: {city}"
    )

    city_entry.delete(0, "end")
    city_entry.insert(0, city)

    weather = get_weather_by_coordinates(lat, lon)

    if weather:
        update_weather_labels(weather)


# Title
title_label = ctk.CTkLabel(
    app,
    text="🌤 Weather Forecast",
    font=("Arial", 30, "bold")
)
title_label.pack(pady=20)

# Location Label
location_label = ctk.CTkLabel(
    app,
    text="📍 Detecting Location...",
    font=("Arial", 16)
)
location_label.pack(pady=5)

# City Entry
city_entry = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Enter city name"
)
city_entry.pack(pady=15)

# Search Button
search_button = ctk.CTkButton(
    app,
    text="Search Weather",
    command=search_weather,
    width=180,
    height=40
)
search_button.pack(pady=10)

# Divider
divider = ctk.CTkLabel(
    app,
    text="━━━━━━━━━━━━━━━━━━━━━━━━━━"
)
divider.pack(pady=15)

# Weather Labels
temperature_label = ctk.CTkLabel(
    app,
    text="🌡 Temperature: --",
    font=("Arial", 18)
)
temperature_label.pack(pady=10)

humidity_label = ctk.CTkLabel(
    app,
    text="💧 Humidity: --",
    font=("Arial", 18)
)
humidity_label.pack(pady=10)

wind_label = ctk.CTkLabel(
    app,
    text="🌬 Wind Speed: --",
    font=("Arial", 18)
)
wind_label.pack(pady=10)

condition_label = ctk.CTkLabel(
    app,
    text="☁ Condition: --",
    font=("Arial", 18)
)
condition_label.pack(pady=10)

# Load weather automatically
load_current_location_weather()

# Run App
app.mainloop()