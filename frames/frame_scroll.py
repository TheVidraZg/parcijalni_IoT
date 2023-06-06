import tkinter as tk


class FrmScrollable(tk.Frame):
    def __init__(self, master, background='#333333'):
        super().__init__(master, background=background)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.frm_scrollable = tk.Frame(self.canvas)


        

        self.scrollbar = tk.Scrollbar(self,
                                orient='vertical',
                                command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')


        self.frm_scrollable.bind(
            '<Configure>',
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.frm_scrollable, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)