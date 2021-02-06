import tkinter as tk
from tkinter import ttk

BLACK = "#000000"
DARKEST_GREY = "#111111"
DARKER_GREY = "#1A1A1A"
DARK_GREY = "#212121"
GREY = "#848484"
LIGHT_GREY = "#cccccc"
WHITE = "#F0F0F0"
DARKER_WHITE = "#C7C7C7"
DARK_BLUE = "#3869A5"
LIGHT_BLUE = "#3869A5" #"#7CDDDB"
RED = "#6F1A07"

class ThemeManager:
    """
    Used to manage all custom themes.\n
    master should be tk.TK
    """
    def __init__(self, master):
        self.master = master
        self.style = ttk.Style(master)
        self.style_options = {}
        self.style_colors = {}
        self.default_theme = self.style.theme_use()
        self.default_options = []
        self.default_options.append(("*Text*background", "#FFFFFF"))
        self.default_options.append(("*Text*foreground", "#000000"))

        self.create_TKC("darkTKC", DARKER_GREY, DARKER_WHITE, DARK_GREY, DARK_BLUE, GREY)
        self.create_TKC("lightTKC", WHITE, DARKER_GREY, LIGHT_GREY, LIGHT_BLUE, GREY)

    def set_theme(self, name):
        """
        To get the available theme names use get_themes.\n
        It's recommended to use TKC themes
        """
        self.style.theme_use(name)
        self.set_colors(name)
        self.set_options(name)
        self.change_toplevel()
        self.add_additional()
    
    def create_TKC(self, name, background, foreground, highlight, active, disabled):
        """
        Creates a different color variant of the TKC theme.
        (just a reskin of alt theme)
        """
        FOREGROUND = foreground
        BACKGROUND = background
        HIGHLIGHT = highlight
        ACTIVE = active
        DISABLED = disabled
        self.style_colors[name] = {}
        self.style_colors[name]['foreground'] = foreground
        self.style_colors[name]['background'] = background
        self.style_colors[name]['highlight'] = highlight
        self.style_colors[name]['active'] = active
        self.style_colors[name]['disabled'] = disabled

        self.style_options[name] = []
        self.style.theme_create(name, parent='alt')
        self.style.theme_use(name)
        self.style.configure(".",
                             background=BACKGROUND,
                             foreground=FOREGROUND,
                             font='Consolas 10',
                             troughcolor=BACKGROUND,
                             insertcolor=FOREGROUND,
                             indicatorcolor=BACKGROUND,
                             fieldbackground=BACKGROUND,
                             highlightcolor=HIGHLIGHT,
                             arrowcolor=FOREGROUND
                             #borderwidth=0
                            )

        #Toolbutton
        self.style.map("Toolbutton",
                       foreground=[('active', ACTIVE), ('selected', ACTIVE)],
                       background=[('active', HIGHLIGHT)],
                      )
        # BUTTON
        self.style.configure("TButton",
                             highlightthickness=2,
                             borderwidth=1,
                             relief="groove",
                             padding=3,
                            )
        self.style.map("TButton",
                       foreground=[('active', ACTIVE), ("pressed", ACTIVE), ('disabled', DISABLED)],
                       background=[('active', "!pressed", HIGHLIGHT)],
                      )
        self.style.layout("TButton",
                          [["Button.border",
                          {
                              "sticky": "nswe",
                              "border": "1",
                              "children": [
                                  [
                                      
                                          "Button.padding",
                                          {
                                              "sticky": "nswe",
                                              "children": [
                                                  [
                                                      "Button.label",
                                                      {
                                                          "sticky": "nswe"
                                                      }
                                                  ]
                                              ]
                                          }
                                      
                                  ]
                              ]
                          }]])
        # Entry
        self.style.configure("TEntry",
                             highlightthickness=1,
                             borderwidth=1,
                             relief="ridge",
                             padding=2,
                            )
        #Label
        self.style.map("TLabel",
            foreground=[('selected', FOREGROUND)],
            background=[('selected', HIGHLIGHT)]
        )
        #Scrollbars
        self.style.configure("Horizontal.Scrollbar",
            arrowsize=5,
            borderwidth=1,
        )
        self.style.configure("Vertical.Scrollbar",
            arrowsize=5,
            borderwidth=1,
        )
        #Checkbutton
        self.style.configure("TCheckbutton",
                             indicatormargin=3,
                             borderwidth=2,
                             indicatorrelief="GROOVE",
                             indicatordiameter=12
        )
        self.style.map("TCheckbutton",
            indicatorcolor=[('selected', ACTIVE)],
        )
        #TRadiobutton
        self.style.map("TRadiobutton",
            indicatorcolor=[('selected', ACTIVE)],
            foreground=[('disabled', DISABLED)]
        )
        #TRadiobutton button version
        self.style.map("TRadiobutton.TButton",
            foreground=[('active', ACTIVE), ("selected", ACTIVE)],
            background=[('active', "!selected", HIGHLIGHT), ("selected", BACKGROUND)]
        )
        #Combobox
        self.style.configure("TCombobox",
            arrowsize=15
        )
        self.style.map("TCombobox",
            background=[('hover', HIGHLIGHT)],
            arrowcolor=[('hover', ACTIVE)]
        )
        self.style_options[name].append(("*TCombobox*Listbox.background", BACKGROUND))
        self.style_options[name].append(("*TCombobox*Listbox.foreground", FOREGROUND))
        self.style_options[name].append(("*TCombobox*Listbox.selectBackground", HIGHLIGHT))
        self.style_options[name].append(("*TCombobox*Listbox.selectForeground", ACTIVE))
        #Treeview
        self.style.map("Treeview",
            background=[('selected', HIGHLIGHT)],
            foreground=[('selected', ACTIVE)]
        )
        self.style.configure("Item",
            focuscolor=BACKGROUND
        )
        self.style.map("Item",
            focuscolor=[('selected', HIGHLIGHT)]
        )
        #Notebook
        self.style.configure("TNotebook",
            borderwidth=0
        )
        self.style.configure("TNotebook.Tab",
            padding=(5, 2),
            borderwidth=0
        )
        self.style.map("TNotebook.Tab",
            foreground=[('active', ACTIVE), ('selected', ACTIVE)],
            background=[('active', HIGHLIGHT), ('selected', HIGHLIGHT)]
        )
        #Text
        self.style_options[name].append(("*Text*background", BACKGROUND))
        self.style_options[name].append(("*Text*foreground", FOREGROUND))
        self.style_options[name].append(("*Text*insertBackground", FOREGROUND))

    def set_options(self, name):
        """
        sets the options for the curent style
        """
        if name not in self.style_options:
            return
        for option in self.style_options[name]:
            self.master.option_add(*option)

    def set_colors(self, name):
        """
        sets colors for not ttk widgets
        """
        if name not in self.style_colors:
            return
        self.master.tk_setPalette(background=self.style_colors[name]["background"],
                                 foreground=self.style_colors[name]["foreground"],
                                 insertBackground=self.style_colors[name]["foreground"],
                                 selectBackground=self.style_colors[name]["highlight"],
                                 selectForeground=self.style_colors[name]["active"],
                                 )


    def change_toplevel(self):
        """
        Changes color of all the tk.toplevel under master
        """
        background = self.style.lookup(".", "background")
        self.master["bg"] = background

        for k, child in self.master.children.items():
            if isinstance(child, tk.Toplevel):
                child["bg"] = background

    def get_themes(self):
        """
        Returns available theme names.
        """
        return self.style.theme_names()

    def lookup(self, style_, option):
        """
        looks up the value of option in the style. \n
        for ex. the background color, foreground color.
        """
        return self.style.lookup(style_, option)

    def add_additional(self):
        """
        Adds additional styles that are used by tkc
        """
        self.style.configure("Error.TEntry",
            foreground=RED
        )

if __name__ == "__main__":
    tk = tk.Tk()
    thememan = ThemeManager(tk)
    tk.mainloop()