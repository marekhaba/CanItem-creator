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
    Base clas for all other edits
     validate command should be a function that returns true or false
     on_valid command that will run if the validate command returns true
     on_invalid command that will run if the validate command returns false
     default - value that gets set when Edit is empty - ""
     change_output - func gets called on valid output
    """
    def __init__(self, master, name, *args, **kwargs):
        self.validate_command = kwargs.pop("validate", None)
        self.on_valid = kwargs.pop("on_valid", None)
        self.on_invalid = kwargs.pop("on_invalid", None)
        self.default = kwargs.pop("default", "")
        self.last_valid = self.default
        self.change_output = kwargs.pop("change_output", lambda v: v)

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

    def _set_default(self, *args):
        #subclasses should have a way to call this emthod
        if self.default != "" and self.var.get() == "":
            self.set(self.default)

    def get(self):
        """
        Returns value of this edit.
        """
        if self.validate_command is not None:
            if self.validate_command(self.var.get()):
                self.last_valid = self.change_output(self.var.get())
                if self.on_valid is not None:
                    self.on_valid()
            elif self.on_invalid is not None:
                self.on_invalid()
            return self.last_valid
        return self.change_output(self.var.get())

    def get_name(self):
        """
        returns name of this edit
        """
        return self.name

class StrEdit(BaseEdit):
    """
    Returns str
    """
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 10)
        super().__init__(master, name, *args, **kwargs)

        self.entry = ttk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.pack(side="left", padx=3, pady=3)
        self.entry.bind("FocusOut", self._set_default, True)

class IntEdit(BaseEdit):
    """
    Returns int
    """
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 3)
        if "validate" not in kwargs:
            kwargs["validate"] = self._validate_callback
        super().__init__(master, name, *args, **kwargs)
        
        self.change_output = int

        if self.default == "":
            self.default = 1
        self.set(self.default)

        self.entry = ttk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.pack(side="left", padx=3, pady=3)
        self.entry.bind("<FocusOut>", self._set_default, True)

    def _validate_callback(self, string):
        try:
            int(string)
            return True
            #self.entry["style"] = "TEntry" TODO This will be moved to on_in/valid when I will finish themes
        except ValueError:
            #self.entry["style"] = "Error.TEntry"
            return False

class ColorEdit(BaseEdit):
    """
    Choice of ttk color
    """#TODO expand this edit
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 9)
        super().__init__(master, name, *args, **kwargs)
        self.combobox = ttk.Combobox(self, values=COLORS, textvariable=self.var, width=entry_width)
        self.combobox.pack(side="left", padx=3, pady=3)

class AnchorEdit(BaseEdit):
    def __init__(self, master, name, *args, **kwargs):
        entry_width = kwargs.pop("entry_width", 6)
        super().__init__(master, name, *args, **kwargs)
        _anchors = ("n", "nw", "ne", "w", "center", "e", "sw", "s", "se")
        self.combobox = ttk.Combobox(self, values=_anchors, textvariable=self.var, width=entry_width, state=("readonly",))
        self.combobox.pack(side="left", padx=3, pady=3)
        self.set("center")
