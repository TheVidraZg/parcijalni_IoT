import requests
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to fetch weather data from the source URL
def fetch_weather_data():
    url = "https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici"
    try:
        response = requests.get(url)
        # Process the response and extract the required data
        # Here, you'll need to parse the XML response and extract the relevant values
        # Update the temperature, humidity, pressure, and clothing icon labels accordingly

        # For demonstration purposes, I'll assume the data is retrieved and processed correctly
        temperature_indoor = 25
        temperature_outdoor = 20
        temperature_city = 18
        humidity_indoor = 60
        humidity_outdoor = 70
        pressure_indoor = 1012
        pressure_outdoor = 1008

        # Update the labels with the retrieved values
        temperature_indoor_label.config(text=f"Indoor Temperature: {temperature_indoor}°C")
        temperature_outdoor_label.config(text=f"Outdoor Temperature: {temperature_outdoor}°C")
        temperature_city_label.config(text=f"City Temperature: {temperature_city}°C")
        humidity_indoor_label.config(text=f"Indoor Humidity: {humidity_indoor}%")
        humidity_outdoor_label.config(text=f"Outdoor Humidity: {humidity_outdoor}%")
        pressure_indoor_label.config(text=f"Indoor Pressure: {pressure_indoor} hPa")
        pressure_outdoor_label.config(text=f"Outdoor Pressure: {pressure_outdoor} hPa")

        # Update the clothing icon based on the temperature
        if temperature_indoor > 22:
            clothing_icon_label.config(text="Obuci kratke rukave")
        elif 12 <= temperature_indoor <= 22:
            clothing_icon_label.config(text="Obucite laganu jaknu")
        elif 0 <= temperature_indoor < 12:
            clothing_icon_label.config(text="Obucite deblju jaknu")
        else:
            clothing_icon_label.config(text="Obucite kapu, sal i zimsku jaknu !")

        # Store the data in the SQLite database
        conn = sqlite3.connect("meteo_data.db")
        c = conn.cursor()
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("temperature_indoor", temperature_indoor))
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("temperature_outdoor", temperature_outdoor))
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("temperature_city", temperature_city))
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("humidity_indoor", humidity_indoor))
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("humidity_outdoor", humidity_outdoor))
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("pressure_indoor", pressure_indoor))
        c.execute("INSERT INTO sensor_data (timestamp, sensor_type, value) VALUES (DATETIME('now'), ?, ?)",
                  ("pressure_outdoor", pressure_outdoor))
        conn.commit()
        conn.close()

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Nemoguce je dohvatiti podatke")

# Create the main Tkinter window
window = tk.Tk()
window.title("Meteo App")
window.geometry('700x700')

# Create labels for displaying temperature, humidity, pressure, and clothing icon
temperature_indoor_label = tk.Label(window, text="Indoor Temperature: -°C")
temperature_outdoor_label = tk.Label(window, text="Outdoor Temperature: -°C")
temperature_city_label = tk.Label(window, text="City Temperature: -°C")
humidity_indoor_label = tk.Label(window, text="Indoor Humidity: -%")
humidity_outdoor_label = tk.Label(window, text="Outdoor Humidity: -%")
pressure_indoor_label = tk.Label(window, text="Indoor Pressure: - hPa")
pressure_outdoor_label = tk.Label(window, text="Outdoor Pressure: - hPa")
clothing_icon_label = tk.Label(window, text="Clothing Icon: -")

# Create a button to fetch weather data
fetch_button = tk.Button(window, text="Dohvati podatke", command=fetch_weather_data)

# Place the labels and button in the window
temperature_indoor_label.pack()
temperature_outdoor_label.pack()
temperature_city_label.pack()
humidity_indoor_label.pack()
humidity_outdoor_label.pack()
pressure_indoor_label.pack()
pressure_outdoor_label.pack()
clothing_icon_label.pack()
fetch_button.pack()

# Create the SQLite database and sensor_data table
conn = sqlite3.connect("meteo_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (timestamp TIMESTAMP, sensor_type TEXT, value REAL)''')
conn.commit()
conn.close()

# Start the Tkinter event loop
window.mainloop()
