import tkinter as tk
import datetime as dt
from sqlalchemy import Column, Integer, String, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import xml.etree.ElementTree as ET

Base = declarative_base()

class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    temperature = Column(String)
    humidity = Column(String)
    pressure = Column(String)
    outdoor_temperature = Column(String)
    outdoor_humidity = Column(String)
    outdoor_pressure = Column(String)
    


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

        self.db_url = 'sqlite:///C:/py_code-learning/py_code-learning_Parcijalni_IoT/parcijalni_IoT/meteo_app.db'
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
        self.labels[0].config(text=f"Unutarnja Temperatura: {temperature}")
        self.labels[1].config(text=f"Vanjska Temperatura: {outdoor_temp}")
        self.labels[2].config(text=f"Vlaznost zraka: {humidity}")
        self.labels[3].config(text=f"Vlaznost zraka(vani): {outdoor_hum}")
        self.labels[4].config(text=f"Unutarnji pritisak zraka: {pressure} ")
        self.labels[5].config(text=f"Vanjski Pritisak zraka: {outdoor_press} ")


        outdoor_temp_deg = outdoor_temp.split('°')[0]  

        if float(outdoor_temp_deg) > 22:
            self.clothing_icon_label.config(text="Obuci kratke rukave")
        elif 12 <= float(outdoor_temp_deg) <= 22:
            self.clothing_icon_label.config(text="Obucite laganu jaknu")
        elif 0 <= float(outdoor_temp_deg) < 12:
            self.clothing_icon_label.config(text="Obucite deblju jaknu")
        else:
            self.clothing_icon_label.config(text="Obucite kapu, sal i zimsku jaknu !")

    def fetch_data(self):
        temperature = '22°C'
        humidity = '50%'
        pressure = '1014 hPa'
    
        url = "https://vrijeme.hr/hrvatska_n.xml"
        response = requests.get(url)
        xml_data = response.content

        root = ET.fromstring(xml_data)
        for grad in root.iter('Grad'):
            grad_ime = grad.find('GradIme').text
            if grad_ime == 'Zagreb-Maksimir':
                outdoor_temp = grad.find('Podatci/Temp').text + "°C"
                outdoor_hum = grad.find('Podatci/Vlaga').text + "%"
                outdoor_press = grad.find('Podatci/Tlak').text + " hPa"
                break
        
        engine = create_engine(self.db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        inspector = inspect(engine)
        if not inspector.has_table(Measurement.__tablename__):
            Base.metadata.create_all(engine)
            print("Created table 'measurements'.")

        measurement = Measurement(temperature=temperature,
                                  humidity=humidity,
                                  pressure=pressure,
                                  outdoor_temperature=outdoor_temp,
                                  outdoor_humidity=outdoor_hum,
                                  outdoor_pressure=outdoor_press)
        session.add(measurement)
        session.commit()
        session.close()
        self.update_data(temperature, outdoor_temp, humidity, outdoor_hum, pressure, outdoor_press)