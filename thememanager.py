import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """
    Used to manage all custom themes.\n
    master should be tk.TK
    """
    def __init__(self, master):
        self.master = master
        self.style = ttk.Style(master)
        #print(self.style.lookup("TButton", "foreground", ("pressed",)))
        self.style.map("TRadiobutton.TButton",
            foreground=[("active", self.style.lookup("TButton", "foreground", ("pressed",)))],
            background=[("active", self.style.lookup("TButton", "background", ("pressed",)))]
        )

if __name__ == "__main__":
    tk = tk.Tk()
    thememan = ThemeManager(tk)
    tk.mainloop()