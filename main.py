import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from weather_api import (
    get_weather,
    get_weather_by_coordinates
)
from location import get_location

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Advanced Weather Dashboard")
app.geometry("1000x850")
app.resizable(False, False)

current_lat = None
current_lon = None
current_weather = None
search_history = []

# WEATHER ICONS

def get_weather_icon(condition):
    c = condition.lower()

    if "clear" in c:
        return "☀️"
    if "cloud" in c:
        return "☁️"
    if "rain" in c:
        return "🌧️"
    if "thunder" in c:
        return "⛈️"
    if "snow" in c:
        return "❄️"

    return "🌤️"

# CLOCK

def update_clock():
    now = datetime.now()

    date_label.configure(
        text=now.strftime("%A, %d %B %Y")
    )

    time_label.configure(
        text=now.strftime("%I:%M:%S %p")
    )

    app.after(1000, update_clock)

# SEARCH HISTORY

def add_history(city):
    if city in search_history:
        search_history.remove(city)

    search_history.insert(0, city)

    if len(search_history) > 5:
        search_history.pop()

    history_box.configure(state="normal")
    history_box.delete("1.0", "end")

    for item in search_history:
        history_box.insert("end", f"• {item}\n")

    history_box.configure(state="disabled")

# UPDATE WEATHER

def update_weather(data):
    global current_weather

    current_weather = data

    weather_icon.configure(
        text=get_weather_icon(data["condition"])
    )

    city_label.configure(
        text=data["city"]
    )

    temp_label.configure(
        text=f"{round(data['temperature'])}°C"
    )

    condition_label.configure(
        text=data["condition"]
    )

    humidity_value.configure(
        text=f"{data['humidity']}%"
    )

    wind_value.configure(
        text=f"{data['wind']} m/s"
    )

    feels_value.configure(
        text=f"{round(data['feels_like'])}°C"
    )

    pressure_value.configure(
        text=f"{data['pressure']} hPa"
    )

    visibility_value.configure(
        text=f"{data['visibility']} km"
    )

    sunrise_value.configure(
        text=data["sunrise"]
    )

    sunset_value.configure(
        text=data["sunset"]
    )

# SEARCH WEATHER

def search_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror(
            "Error",
            "Please enter a city name."
        )
        return

    weather = get_weather(city)

    if not weather:
        messagebox.showerror(
            "Error",
            "City not found."
        )
        return

    add_history(weather["city"])
    update_weather(weather)

# AUTO LOCATION

def load_location_weather():
    global current_lat, current_lon

    loc = get_location()

    if not loc:
        location_label.configure(
            text="📍 Location not detected"
        )
        return

    current_lat = loc["lat"]
    current_lon = loc["lon"]

    weather = get_weather_by_coordinates(
        current_lat,
        current_lon
    )

    if weather:
        location_label.configure(
            text=f"📍 Current Location: {loc['city']}"
        )

        city_entry.delete(0, "end")
        city_entry.insert(0, weather["city"])

        add_history(weather["city"])
        update_weather(weather)

# REFRESH WEATHER

def refresh_weather():
    if current_lat is None:
        return

    weather = get_weather_by_coordinates(
        current_lat,
        current_lon
    )

    if weather:
        update_weather(weather)

# THEME SWITCH

def toggle_theme():
    if theme_switch.get():
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")


# EXPORT REPORT

def export_report():
    if not current_weather:
        messagebox.showerror(
            "Error",
            "No weather data available."
        )
        return

    report = f"""
Weather Report
=================

City: {current_weather['city']}
Temperature: {current_weather['temperature']}°C
Feels Like: {current_weather['feels_like']}°C
Humidity: {current_weather['humidity']}%
Pressure: {current_weather['pressure']} hPa
Visibility: {current_weather['visibility']} km
Wind Speed: {current_weather['wind']} m/s
Condition: {current_weather['condition']}
Sunrise: {current_weather['sunrise']}
Sunset: {current_weather['sunset']}

Generated On:
{datetime.now()}
"""

    with open(
        "weather_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    messagebox.showinfo(
        "Success",
        "Weather report exported successfully."
    )


# HEADER

title = ctk.CTkLabel(
    app,
    text="Weather Dashboard",
    font=("Arial", 34, "bold")
)
title.pack(pady=10)

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
time_label.pack()

location_label = ctk.CTkLabel(
    app,
    text="📍 Detecting location...",
    font=("Arial", 18)
)
location_label.pack(pady=10)

# SEARCH BAR

top_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
top_frame.pack(pady=10)

city_entry = ctk.CTkEntry(
    top_frame,
    width=350,
    height=40,
    placeholder_text="Enter city name"
)
city_entry.grid(row=0, column=0, padx=10)

ctk.CTkButton(
    top_frame,
    text="Search",
    command=search_weather
).grid(row=0, column=1, padx=5)

ctk.CTkButton(
    top_frame,
    text="Refresh",
    command=refresh_weather
).grid(row=0, column=2, padx=5)

ctk.CTkButton(
    top_frame,
    text="Export Report",
    command=export_report
).grid(row=0, column=3, padx=5)

theme_switch = ctk.CTkSwitch(
    app,
    text="Light Mode",
    command=toggle_theme
)
theme_switch.pack()

# WEATHER CARD

weather_card = ctk.CTkFrame(
    app,
    corner_radius=20
)
weather_card.pack(
    pady=15,
    padx=20,
    fill="x"
)

weather_icon = ctk.CTkLabel(
    weather_card,
    text="🌤️",
    font=("Arial", 70)
)
weather_icon.pack(pady=(15, 5))

temp_label = ctk.CTkLabel(
    weather_card,
    text="--°C",
    font=("Arial", 54, "bold")
)
temp_label.pack()

city_label = ctk.CTkLabel(
    weather_card,
    text="City",
    font=("Arial", 26, "bold")
)
city_label.pack()

condition_label = ctk.CTkLabel(
    weather_card,
    text="Condition",
    font=("Arial", 18)
)
condition_label.pack(pady=(0, 15))

# WEATHER DETAILS

details = ctk.CTkFrame(app)
details.pack(
    padx=20,
    pady=10,
    fill="x"
)

labels = [
    ("Humidity", "humidity_value"),
    ("Wind", "wind_value"),
    ("Feels Like", "feels_value"),
    ("Pressure", "pressure_value"),
    ("Visibility", "visibility_value"),
    ("Sunrise", "sunrise_value"),
    ("Sunset", "sunset_value"),
]

widgets = {}

for i, (name, var) in enumerate(labels):
    ctk.CTkLabel(
        details,
        text=name,
        font=("Arial", 16, "bold")
    ).grid(
        row=i // 2,
        column=(i % 2) * 2,
        padx=20,
        pady=8,
        sticky="w"
    )

    widgets[var] = ctk.CTkLabel(
        details,
        text="--",
        font=("Arial", 16)
    )

    widgets[var].grid(
        row=i // 2,
        column=(i % 2) * 2 + 1,
        padx=10,
        pady=8,
        sticky="w"
    )

humidity_value = widgets["humidity_value"]
wind_value = widgets["wind_value"]
feels_value = widgets["feels_value"]
pressure_value = widgets["pressure_value"]
visibility_value = widgets["visibility_value"]
sunrise_value = widgets["sunrise_value"]
sunset_value = widgets["sunset_value"]

# SEARCH HISTORY

history_frame = ctk.CTkFrame(app)
history_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

ctk.CTkLabel(
    history_frame,
    text="Recent Searches",
    font=("Arial", 18, "bold")
).pack(pady=5)

history_box = ctk.CTkTextbox(
    history_frame,
    height=100
)
history_box.pack(
    fill="x",
    padx=10,
    pady=10
)

history_box.configure(state="disabled")

# START APP

update_clock()
load_location_weather()

app.mainloop()