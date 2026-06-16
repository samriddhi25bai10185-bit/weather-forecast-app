import customtkinter as ctk

# App Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create Window
app = ctk.CTk()
app.title("Weather Forecast")
app.geometry("500x550")
app.resizable(False, False)

# Title
title_label = ctk.CTkLabel(
    app,
    text="🌤 Weather Forecast",
    font=("Arial", 28, "bold")
)
title_label.pack(pady=20)

# City Entry
city_entry = ctk.CTkEntry(
    app,
    width=300,
    height=40,
    placeholder_text="Enter city name"
)
city_entry.pack(pady=10)

# Search Button
search_button = ctk.CTkButton(
    app,
    text="Search",
    width=150,
    height=40
)
search_button.pack(pady=10)

# Divider
divider = ctk.CTkLabel(app, text="━━━━━━━━━━━━━━━━━━━━")
divider.pack(pady=10)

# Weather Info Labels
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

# Footer
footer_label = ctk.CTkLabel(
    app,
    text="Python Weather Forecast App",
    font=("Arial", 12)
)
footer_label.pack(side="bottom", pady=15)

# Run App
app.mainloop()