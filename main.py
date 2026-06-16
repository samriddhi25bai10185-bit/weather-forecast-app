import customtkinter as ctk

# App Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create Window
app = ctk.CTk()
app.title("Weather Forecast")
app.geometry("500x500")

# Title
title_label = ctk.CTkLabel(
    app,
    text="Weather Forecast",
    font=("Arial", 28, "bold")
)
title_label.pack(pady=20)

# City Entry
city_entry = ctk.CTkEntry(
    app,
    width=250,
    height=40,
    placeholder_text="Enter city name"
)
city_entry.pack(pady=10)

# Search Button
search_button = ctk.CTkButton(
    app,
    text="Search",
    width=120,
    height=40
)
search_button.pack(pady=10)

# Weather Information
temperature_label = ctk.CTkLabel(
    app,
    text="Temperature: --",
    font=("Arial", 18)
)
temperature_label.pack(pady=10)

humidity_label = ctk.CTkLabel(
    app,
    text="Humidity: --",
    font=("Arial", 18)
)
humidity_label.pack(pady=10)

wind_label = ctk.CTkLabel(
    app,
    text="Wind Speed: --",
    font=("Arial", 18)
)
wind_label.pack(pady=10)

condition_label = ctk.CTkLabel(
    app,
    text="Condition: --",
    font=("Arial", 18)
)
condition_label.pack(pady=10)

app.mainloop()