import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from weather_api import get_weather, get_weather_by_coordinates
from location import get_location

# -----------------------------
# APP SETTINGS
# -----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Weather Forecast Dashboard")
app.geometry("700x700")
app.resizable(False, False)

current_lat = None
current_lon = None


# -----------------------------
# WEATHER ICONS
# -----------------------------
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


# -----------------------------
# LIVE CLOCK
# -----------------------------
def update_time():
    now = datetime.now()

    date_text = now.strftime("%A, %d %B %Y")
    time_text = now.strftime("%I:%M:%S %p")

    date_label.configure(text=date_text)
    time_label.configure(text=time_text)

    app.after(1000, update_time)


# -----------------------------
# UPDATE WEATHER UI
# -----------------------------
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


# -----------------------------
# SEARCH WEATHER
# -----------------------------
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


# -----------------------------
# LOAD CURRENT LOCATION
# -----------------------------
def load_current_location_weather():
    global current_lat, current_lon

    location = get_location()

    if location is None:
        location_text.configure(
            text="📍 Location Not Detected"
        )
        return

    city = location["city"]
    current_lat = location["lat"]
    current_lon = location["lon"]

    location_text.configure(
        text=f"📍 Current Location: {city}"
    )

    city_entry.delete(0, "end")
    city_entry.insert(0, city)

    weather = get_weather_by_coordinates(
        current_lat,
        current_lon
    )

    if weather:
        update_weather(weather)


# -----------------------------
# REFRESH WEATHER
# -----------------------------
def refresh_weather():
    if current_lat is None:
        return

    weather = get_weather_by_coordinates(
        current_lat,
        current_lon
    )

    if weather:
        update_weather(weather)


# -----------------------------
# TITLE
# -----------------------------
title_label = ctk.CTkLabel(
    app,
    text="Weather Forecast Dashboard",
    font=("Arial", 32, "bold")
)
title_label.pack(pady=15)

# -----------------------------
# DATE & TIME
# -----------------------------
date_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 16)
)
date_label.pack()

time_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 18, "bold")
)
time_label.pack(pady=5)

# -----------------------------
# LOCATION
# -----------------------------
location_text = ctk.CTkLabel(
    app,
    text="📍 Detecting Location...",
    font=("Arial", 16)
)
location_text.pack(pady=10)

# -----------------------------
# SEARCH BAR
# -----------------------------
search_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
search_frame.pack(pady=10)

city_entry = ctk.CTkEntry(
    search_frame,
    width=300,
    height=40,
    placeholder_text="Enter city name"
)
city_entry.grid(row=0, column=0, padx=10)

search_button = ctk.CTkButton(
    search_frame,
    text="Search",
    command=search_weather,
    width=120
)
search_button.grid(row=0, column=1)

# -----------------------------
# WEATHER CARD
# -----------------------------
weather_card = ctk.CTkFrame(
    app,
    width=550,
    height=250,
    corner_radius=20
)
weather_card.pack(pady=20)

weather_icon = ctk.CTkLabel(
    weather_card,
    text="🌤️",
    font=("Arial", 70)
)
weather_icon.pack(pady=(20, 5))

temp_label = ctk.CTkLabel(
    weather_card,
    text="--°C",
    font=("Arial", 50, "bold")
)
temp_label.pack()

city_label = ctk.CTkLabel(
    weather_card,
    text="City",
    font=("Arial", 24)
)
city_label.pack()

condition_label = ctk.CTkLabel(
    weather_card,
    text="Condition",
    font=("Arial", 18)
)
condition_label.pack(pady=(0, 15))

# -----------------------------
# DETAILS CARD
# -----------------------------
details_frame = ctk.CTkFrame(
    app,
    width=550,
    height=120,
    corner_radius=20
)
details_frame.pack(pady=10)

humidity_title = ctk.CTkLabel(
    details_frame,
    text="Humidity",
    font=("Arial", 18, "bold")
)
humidity_title.grid(row=0, column=0, padx=50, pady=15)

wind_title = ctk.CTkLabel(
    details_frame,
    text="Wind Speed",
    font=("Arial", 18, "bold")
)
wind_title.grid(row=0, column=1, padx=50)

humidity_value = ctk.CTkLabel(
    details_frame,
    text="--",
    font=("Arial", 24)
)
humidity_value.grid(row=1, column=0)

wind_value = ctk.CTkLabel(
    details_frame,
    text="--",
    font=("Arial", 24)
)
wind_value.grid(row=1, column=1)

# -----------------------------
# REFRESH BUTTON
# -----------------------------
refresh_button = ctk.CTkButton(
    app,
    text="Refresh Current Location Weather",
    command=refresh_weather,
    width=260,
    height=40
)
refresh_button.pack(pady=20)

# -----------------------------
# START APP
# -----------------------------
update_time()
load_current_location_weather()

app.mainloop()