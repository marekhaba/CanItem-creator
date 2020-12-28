"""
Contains widgets for modifying item options and for selecting what tool is beung used.
"""
import tkinter as tk
from tkinter import ttk
import items

class OptionsBar(ttk.Frame):
    """
    Manages all options for the item
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.frames = {}#{key: ttk.Frame(self) for key in items.ITEMS}
        for item, info in items.ITEMS.items():
            self.frames[item] = ttk.Frame(self)
            for option in info["basic"]:
                edit = items.OPTIONS[option]["edit"](self.frames[item], option)
                edit.pack(side="left", padx=3, pady=3)

        self.current = None
        #self.fill_edit.show()

    def change_frame(self, name):
        """
        Changes the what options are displayed
        """
        if self.current is not None:
            self.frames[self.current].pack_forget()
        if name not in self.frames:
            self.current = None
            return
        self.frames[name].pack()
        self.current = name

    def get(self):
        """
        returns kwargs of the options.
        """
        if self.current is None:
            return {}
        options = {}
        for edit in self.frames[self.current].winfo_children():
            if edit.get() == "":
                continue
            options[edit.get_name()] = edit.get()
        return options


class ToolBar(ttk.Frame):
    """
    Manages choice of different tools.\n
    To get the current tool use .get()
    """
    def __init__(self, master, optionsbar: OptionsBar, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.tools = {}
        self.tool = tk.StringVar()
        self.optionsbar = optionsbar
        self.tool.trace_add("write", lambda *e: self.optionsbar.change_frame(self.tool.get()))

    def add_tool(self, name: str, image=None):
        """
        Adds tool to the toolbar if image is None, name will be used as label.
        """
        self.tools[name] = ttk.Radiobutton(self, variable=self.tool, value=name, text=name,
                                           image=image, style="Toolbutton")
        self.tools[name].pack(side="top", padx=3, pady=3, ipadx=3, ipady=3)

    def get(self):
        """
        Gets the name of the current tool.
        """
        return self.tool.get()

    def set_tool(self, tool):
        """
        Sets the curent tool to the passed tool.
        """
        self.tool.set(tool)
