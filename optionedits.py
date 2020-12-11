"""
different options to edit values
"""
import tkinter as tk
from tkinter import ttk

COLORS = ["white", "grey", "black",
          "yellow", "orange", "red",
          "pink", "violet", "purple",
          "light blue", "blue", "cyan",
          "lime", "olive", "green"]

class ColorEdit(ttk.Frame):
    """
    Choice of ttk color
    """
    def __init__(self, master, name, *args, entry_width=None, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name

        self.label = ttk.Label(self, text=f"{name} =")
        self.label.pack(side="left", padx=3, pady=3)
        self.var = tk.StringVar()
        self.combobox = ttk.Combobox(self, values=COLORS, textvariable=self.var, width=entry_width)
        self.combobox.pack(side="left", padx=3, pady=3)

    def get_name(self):
        """
        returns name of this edit
        """
        return self.name

    def get(self):
        """
        returns value of this edit
        """
        return self.var.get()

class IntEdit(ttk.Frame):
    """
    Returns int
    """
    def __init__(self, master, name, *args, default=1, entry_width=None, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.valid = False
        self.default = default
        self.name = name

        self.label = ttk.Label(self, text=f"{name} =")
        self.label.pack(side="left", padx=3, pady=3)
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.bind("<FocusOut>", lambda e: self._validate_callback(), True)
        self.entry.pack(side="left", padx=3, pady=3)

        self.set(default)

    def set(self, value):
        """
        Sets value of this edit.
        """
        self.var.set(value)

    def get(self):
        """
        Returns value of this edit.\n
        If value is not int will return default
        """
        self._validate_callback()
        if self.valid:
            return int(self.var.get())
        else:
            return self.default

    def get_name(self):
        """
        returns name of this edit
        """
        return self.name

    def _validate_callback(self):
        string = self.var.get()
        try:
            int(string)
            self.valid = True
            #self.entry["style"] = "TEntry"
        except ValueError:
            #self.entry["style"] = "Error.TEntry"
            self.valid = False

class StrEdit(ttk.Frame):
    """
    Returns str
    """
    def __init__(self, master, name, *args, entry_width=None, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name

        self.label = ttk.Label(self, text=f"{name} =")
        self.label.pack(side="left", padx=3, pady=3)
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.pack(side="left", padx=3, pady=3)

    def set(self, value):
        """
        Sets value of this edit.
        """
        self.var.set(value)

    def get(self):
        """
        Returns value of this edit.
        """
        return self.var.get()

    def get_name(self):
        """
        returns name of this edit
        """
        return self.name
