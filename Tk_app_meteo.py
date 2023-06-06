import tkinter as tk
from frames.frame_met import FrmMeteo, FrmTemp




class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title('Meteo-App-Alg')
        self.geometry('600x600')

        self.frm_meteo = FrmMeteo(self)
        self.frm_meteo.pack(fill='x', padx=10, pady=(0, 0))


        self.frm_temp = FrmTemp(self, items_number=7)
        self.frm_temp.pack(fill='x', padx=10, pady=(0, 0), expand=True)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        

tk_app = MainWindow()
tk_app.mainloop()
