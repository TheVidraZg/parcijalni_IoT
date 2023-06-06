import tkinter as tk
import datetime as dt

now = dt.datetime.now().replace(microsecond=0)

class FrmMeteo(tk.Frame):
    def __init__(self, master, background='lightblue'):
        super().__init__(master, background=background)

        self.grid_columnconfigure(0, weight=1)

        self.lbl_meteo_title = tk.Label(self,
                                        background=background,
                                        text='METEO-App'.upper(),
                                        font=('Verdana', 18))
        self.lbl_meteo_title.grid(row=0, column=0, padx=10, pady=(0,10), sticky='ew')

        self.lbl_meteo_city = tk.Label(self,
                                       background=background,
                                       text='Zagreb',
                                       font=('Verdana', 24))
        self.lbl_meteo_city.grid(row=1, column=0, padx=10, pady=10, sticky='ew')


class FrmTemp(tk.Frame):
    def __init__(self, master, background='#333333', items_number=7):
        super().__init__(master, background=background)

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.lbl_maap_time = tk.Label(self,
                                      foreground='#FFFFFF',
                                      background=background,
                                      text=f'Dobrodosli \n {now}',
                                      font=('Verdana', 13))
        self.lbl_maap_time.grid(row=0, column=0, columnspan=6, padx=10, pady=(10, 0), sticky='ew')

        self.labels = [
            tk.Label(self, text="Indoor Temperature: -°C", font=('Vedrana', 13)),
            tk.Label(self, text="Outdoor Temperature: -°C", font=('Vedrana', 13)),
            tk.Label(self, text="Indoor Humidity: -%", font=('Vedrana', 13)),
            tk.Label(self, text="Outdoor Humidity: -%", font=('Vedrana', 13)),
            tk.Label(self, text="Indoor Pressure: - hPa", font=('Vedrana', 13)),
            tk.Label(self, text="Outdoor Pressure: - hPa", font=('Vedrana', 13)),
            tk.Label(self, text="Clothing Icon: -", font=('Vedrana', 13)),
        ]

        for i, label in enumerate(self.labels):
            label.grid(row=i // 2 + 1, column=i % 2, padx=10, pady=10, sticky='ew')

        self.btn_fetch_data = tk.Button(self.master, text='Dohvati Podatke', command=self.fetch_data)
        self.btn_fetch_data.config(bg='blue', fg='white', width=15, height=2)
        self.btn_fetch_data.pack(pady=(10, 0))
        
        self.clothing_icon_label = tk.Label(self, text="Clothing Icon: -", font=('Vedrana', 13))
        self.clothing_icon_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

    def update_data(self, temperature, outdoor_temp, humidity, outdoor_hum, pressure, outdoor_press):
        self.labels[0].config(text=f"Indoor Temperature: {temperature}")
        self.labels[1].config(text=f"Outdoor Temperature: {outdoor_temp}")
        self.labels[2].config(text=f"Indoor Humidity: {humidity}")
        self.labels[3].config(text=f"Outdoor Humidity: {outdoor_hum}")
        self.labels[4].config(text=f"Indoor Pressure: {pressure} ")
        self.labels[5].config(text=f"Outdoor Pressure: {outdoor_press} ")
        
        outdoor_temp = int(outdoor_temp.split('°')[0])
        
        if outdoor_temp > 22:
            self.clothing_icon_label.config(text="Obuci kratke rukave")
        elif 12 <= outdoor_temp <= 22:
            self.clothing_icon_label.config(text="Obucite laganu jaknu")
        elif 0 <= outdoor_temp < 12:
            self.clothing_icon_label.config(text="Obucite deblju jaknu")
        else:
            self.clothing_icon_label.config(text="Obucite kapu, sal i zimsku jaknu !")

    def fetch_data(self):
        temperature = '25°C'
        humidity = '50%'
        pressure = '1013 hPa'
        outdoor_temp = '28°C'
        outdoor_hum = '70%'
        outdoor_press = '982 hPa'
     

        self.update_data(temperature, outdoor_temp, humidity, outdoor_hum, pressure, outdoor_press)