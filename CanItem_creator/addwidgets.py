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

class BaseEdit(ttk.Frame):
    """
    Returns str
    """
    def __init__(self, master, name, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name

        self.label = ttk.Label(self, text=f"{name} =")
        self.label.pack(side="left", padx=3, pady=3)
        self.var = tk.StringVar()

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

class ColorEdit(BaseEdit):
    """
    Choice of ttk color
    """#TODO expand this edit
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 9)
        super().__init__(master, name, *args, **kwargs)
        self.combobox = ttk.Combobox(self, values=COLORS, textvariable=self.var, width=entry_width)
        self.combobox.pack(side="left", padx=3, pady=3)

class IntEdit(BaseEdit):
    """
    Returns int
    """
    def __init__(self, master, name, *args, default=1, entry_width=None, **kwargs):
        entry_width = kwargs.pop("entry_width", 3)
        super().__init__(master, name, *args, **kwargs)
        self.valid = False
        self.default = default
        

        self.entry = ttk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.bind("<FocusOut>", lambda e: self._validate_callback(), True)
        self.entry.pack(side="left", padx=3, pady=3)

        self.set(default)

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

    def _validate_callback(self):
        string = self.var.get()
        try:
            int(string)
            self.valid = True
            #self.entry["style"] = "TEntry"
        except ValueError:
            #self.entry["style"] = "Error.TEntry"
            self.valid = False

class StrEdit(BaseEdit):
    """
    Returns str
    """
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 10)
        super().__init__(master, name, *args, **kwargs)

        self.entry = ttk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.pack(side="left", padx=3, pady=3)

class AnchorEdit(BaseEdit):
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 6)
        super().__init__(master, name, *args, **kwargs)
        _anchors = ("n", "nw", "ne", "w", "center", "e", "sw", "s", "se")
        self.combobox = ttk.Combobox(self, values=_anchors, textvariable=self.var, width=entry_width, state=("readonly",))
        self.combobox.pack(side="left", padx=3, pady=3)
        self.set("center")
