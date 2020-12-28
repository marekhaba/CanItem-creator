import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile

from addwidgets import IntEdit, StrEdit

from sidebars import OptionsBar, ToolBar
from actionmanager import ActionManager
from codetext import CodeText
from utils import is_float

# def options_to_str(options):
#     """
#     transforms the tkinter options thingy to string
#     """
#     string = ""
#     for option in options.values():
#         if is_float(option[3]) and is_float(option[4]):
#             if float(option[3]) != float(option[4]):
#                 string += f", {option[0]} = {option[4]}"
#             continue
#         if option[3] != option[4]:
#             string += f", {option[0]} = {option[4]}"
#     return string

# def kwargs_to_str(**kwargs):
#     return ', '.join('%s=%r' % x for x in kwargs.items())

# def build_code(canvas: tk.Canvas, canvas_name, canvas_config):
#     """
#     #not really used, replaced with a more fancy way
#     will build code that will recreate all items in canvas
#     returns a string with that code
#     """
#     code = "import tkinter\n\n"
#     code += f"{canvas_name} = tkinter.Canvas({kwargs_to_str(**canvas_config)})\n"
#     code += f"{canvas_name}.pack()\n\n"
#     items = canvas.find("all")
#     for item in items:
#         code += f"{canvas_name}.create_{canvas.type(item)}({args_to_str(canvas.coords(item))}{options_to_str(canvas.itemconfigure(item))})"
#     code += f"\n{canvas_name}.mainloop()"
#     return code

class TkinterPaint(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        DEFAULT_CANVAS_NAME = "ca"

        self.optionsbar = OptionsBar(self)
        self.optionsbar.grid(row=0, column=1, sticky="w", padx=2, pady=2)

        self.toolbar = ToolBar(self, self.optionsbar)
        self.toolbar.grid(row=1, column=0, sticky="n", padx=2, pady=2)

        self.codetext = CodeText(self, width=100, wrap="none", canvas_name=DEFAULT_CANVAS_NAME)
        self.codetext.grid(row=0, column=2, rowspan=3)

        self.canvas = PaintCanvas(self, self.toolbar, self.optionsbar, self.codetext, background="white")
        self.canvas.grid(row=1, column=1, padx=2, pady=2, sticky="n")

        self.menu = tk.Menu(self)
        self["menu"] = self.menu
        self.menu.add_command(label="Save", command=self.save)
        self.menu.add_command(label="Undo", command=ActionManager.undo)
        self.menu.add_command(label="Redo", command=ActionManager.redo)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=2, column=1, sticky="ne")
        self.grid_state = tk.BooleanVar(self)
        self.grid_toggle = ttk.Checkbutton(self.canvas_frame, command=self._toggle_grid, variable=self.grid_state, onvalue=True, offvalue=False, text="show grid")
        self.grid_toggle.pack(side="right", padx=3, pady=3)
        self.grid_state.set(True)
        self.canvas_grid = IntEdit(self.canvas_frame, "grid", entry_width=3)
        self.canvas_grid.var.trace_add("write", self.change_grid)
        self.canvas_grid.pack(side="right", padx=3, pady=3)
        self.canvas_name_edit = StrEdit(self.canvas_frame, "name", entry_width=6) #TODO breaks if it is empty
        self.canvas_name_edit.set(DEFAULT_CANVAS_NAME)
        self.canvas_name_edit.var.trace_add("write", lambda *args: self.configure_canvas(canvas_name=self.canvas_name_edit.get()))
        self.canvas_name_edit.pack(side="left", padx=3, pady=3)
        self.canvas_width_edit = IntEdit(self.canvas_frame, "width", entry_width=4, default=400)
        self.canvas_width_edit.var.trace_add("write", lambda *args: self.configure_canvas(width=self.canvas_width_edit.get()))
        self.canvas_width_edit.pack(side="left", padx=3, pady=3)
        self.canvas_height_edit = IntEdit(self.canvas_frame, "height", entry_width=4, default=400)
        self.canvas_height_edit.var.trace_add("write", lambda *args: self.configure_canvas(height=self.canvas_height_edit.get()))
        self.canvas_height_edit.pack(side="left", padx=3, pady=3)


        self.toolbar.add_tool("cursor")
        self.toolbar.add_tool("line")
        self.toolbar.add_tool("rectangle")
        self.toolbar.add_tool("oval")
        self.toolbar.add_tool("polygon")
        self.toolbar.add_tool("text")
        self.toolbar.add_tool("arc")
        self.toolbar.tool.set("line")

        self.from_x_y_frame = ttk.Frame(self)
        self.from_x_y_var = tk.BooleanVar()
        self.from_x_y_toggle = ttk.Checkbutton(self.from_x_y_frame, variable=self.from_x_y_var, onvalue=True, offvalue=False, text="from_xy", command=self.toggle_xy)
        self.from_x_y_toggle.pack(side="top")
        self.from_x_y_btn = ttk.Button(self.from_x_y_frame, text="Set x,y",command=lambda : self.toolbar.set_tool("set_xy"))
        self.from_x_y_btn["state"] = ("disabled",)
        self.from_x_y_btn.pack(side="top")
        self.from_x_y_frame.grid(row=2, column=0)


    def change_grid(self, *args):
        self.canvas.set_grid(self.canvas_grid.get())

    def _toggle_grid(self):
        self.canvas.show_grid(self.grid_state.get())

    def toggle_xy(self):
        if self.from_x_y_var.get():
            self.codetext.from_xy(self.canvas.from_x, self.canvas.from_y)
            self.from_x_y_btn["state"] = ("!disabled",)
            self.canvas.show_xy()
        else:
            self.codetext.revert_xy()
            self.from_x_y_btn["state"] = ("disabled",)
            self.canvas.remove_xy()
            if self.toolbar.tool.get() == "set_xy":
                self.toolbar.set_tool(None)

    def save(self):
        """
        Saves the content of codetext
        """
        files = [('All Files', '*.*'),  
                ('Python Files', '*.py'), 
                ('Text Document', '*.txt')] 
        file = asksaveasfile(filetypes=files, defaultextension=files)
        if file is None:
            return
        file.write(self.codetext.get('1.0', 'end'))
        file.close()
        #with open(file, "r") as f:
        #    f.write()

    def configure_canvas(self, **kwargs):
        canvas_name = kwargs.pop("canvas_name", None)
        self.canvas.configure(**kwargs)
        self.codetext.configure_canvas(canvas_name=canvas_name, **kwargs)

class PaintCanvas(tk.Canvas):
    """
    tk.Canvas where you can paint stuff,
    """

    def __init__(self, master, toolbar: ToolBar, optionsbar: OptionsBar, codetext_, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.toolbar = toolbar
        self.toolbar.tool.trace_add("write", self.delete_holo)
        self.optionsbar = optionsbar
        self.optionsbar.bind("<FocusOut>", self.delete_holo, True)
        self.codetext = codetext_
        self.create = {
            "line": self.create_line,
            "rectangle": self.create_rectangle,
            "oval": self.create_oval,
            "polygon": self.create_polygon,
            "arc": self.create_arc,
            "text": self.create_text
        }
        #items with n possible coords
        self.n_cord = ["line", "polygon"]
        self.one_cord = ["text"]

        self.curent_coords = []
        self._grid_size = 1
        self.GRID_COLOR = "gray40"
        self._is_grid = True

        #keeps all the <_id>s of items (in reallity they are tags I use them as an _id)
        self.items = set()
        self.holo_item = None

        self.bind("<Button-1>", self.press)
        self.bind("<Motion>", self.motion)
        self.bind("<ButtonRelease-1>", self.release)
        self.bind("<Button-3>", self.press_right)
        
        #used in the functionality that allows scalling from xy
        self.from_x = 0
        self.from_y = 0

    def get_options(self):
        """
        returns options specified for the item
        """
        return self.optionsbar.get()

    def _remove_default_options(self, options, item):
        defaults = self.itemconfigure(item)
        without_defaults = {}
        for option, value in options.items():
            if is_float(defaults[option][3]):
                if float(value) != float(defaults[option][3]):
                    without_defaults[option] = value
                continue
            if value != defaults[option][3]:
                without_defaults[option] = value
        return without_defaults


    def set_grid(self, grid):
        """
        sets the size of grid
        """
        self._grid_size = grid
        self.create_grid()

    def delete_grid(self):
        self.delete("grid")

    def show_grid(self, value):
        """
        True/False
        """
        self._is_grid = value
        if self._is_grid:
            self.create_grid()
        else:
            self.delete_grid()

    def _top_grid(self):
        """
        Sets grid on top of Canvas
        """
        self.tag_raise("grid", "all")

    def create_grid(self):
        """
        displays grid(no way)
        """
        if not self._is_grid:
            return
        self.delete_grid()
        if self._grid_size <= 1:
            return
        for x in range(0, self.winfo_width(), self._grid_size):
            self.create_line(x, 0, x, self.winfo_height(), fill=self.GRID_COLOR, tags=("grid",))
        for y in range(0, self.winfo_height(), self._grid_size):
            self.create_line(0, y, self.winfo_width(), y, fill=self.GRID_COLOR, tags=("grid",))

    def get_items_coords(self):
        """
        returns a dictionary:
            item_id: [cords]
        """
        return {item: map(int, self.coords(item)) for item in self.items}

    def create_item(self, name, *args, **kwargs):
        """
        Creates an item with all the undo, redo, code, etc...
        """
        item = self._create_util(name, *args, **kwargs)
        ActionManager.create_action(
            name=f"created {name}",
            info="None",
            undo=lambda: self._delete_item(item),
            redo=lambda: self._create_util(name, *args, _id=item, **kwargs)
        )
        self._top_grid()

    def _create_util(self, name, *args, **kwargs):
        """
        internal function for creating a item
        sepcify _id kwargs to set a custom id{actualy its a tag but its used like an id} to the widget
        """
        _id = kwargs.pop("_id", None)
        item = self.create[name](*args, **kwargs)
        if _id is None:
            _id = f"i{item}"
        self.itemconfigure(item, tags=(_id,))
        self.items.add(_id)
        self.codetext.add_item(_id, name, *args, **self._remove_default_options(kwargs, item))
        return _id

    def _delete_item(self, item):
        """
        removes the item\n
        also removes from code
        """
        self.codetext.remove_item(item)
        self.items.remove(item)
        self.delete(item)

    def _grid(self, x, y):
        '''
        adjusts x and y to fit the grid size
        '''
        difference = x % self._grid_size
        if difference < self._grid_size//2:
            x = x - difference
        else:
            x = x - difference + self._grid_size
        difference = y % self._grid_size
        if difference < self._grid_size//2:
            y = y - difference
        else:
            y = y - difference + self._grid_size
        return x, y

    def delete_holo(self, *args):
        self.delete(self.holo_item)
        self.holo_item = None

    def motion(self, event):
        event.x, event.y = self._grid(event.x, event.y)
        if self.toolbar.get() == "set_xy":
            if self.holo_item is None:
                self.holo_item = self.create_oval(event.x-3, event.y-3, event.x+3, event.y+3, fill="black", tags=("xy",))
                return
            self.coords(self.holo_item, event.x-3, event.y-3, event.x+3, event.y+3)
            return
        if self.toolbar.get() not in self.create:
            return
        if self.toolbar.get() in self.one_cord:
            if self.holo_item is None:
                self.holo_item = self.create[self.toolbar.get()](event.x, event.y, **self.get_options())
                return
            self.coords(self.holo_item, event.x, event.y)
            return
        if self.holo_item is None:
            return
        if 2 > len(self.curent_coords) <= 4:
            temp_coords = self.curent_coords[:-2]
        else:
            temp_coords = self.curent_coords.copy()
        temp_coords.append(event.x)
        temp_coords.append(event.y)
        self.coords(self.holo_item, *temp_coords)

    def set_xy(self, x, y):
        """
        all xy thing have tag "xy"
        """
        self.from_x = x
        self.from_y = y
        self.remove_xy()
        self.show_xy()
        self.master.toggle_xy()

    def show_xy(self):
        """
        Just shows the grafical thing for the xy
        """
        self.create_oval(self.from_x-3, self.from_y-3, self.from_x+3, self.from_y+3, fill="black", tags=("xy",))
        self.create_text(self.from_x-10, self.from_y, text="x", tags=("xy",))
        self.create_text(self.from_x, self.from_y-10, text="y", tags=("xy",))

    def remove_xy(self):
        self.delete("xy")

    def press(self, event):
        event.x, event.y = self._grid(event.x, event.y)
        if self.toolbar.get() == "set_xy":
            self.set_xy(event.x, event.y)
            self.delete_holo()
        if self.toolbar.get() not in self.create:
            return
        if self.toolbar.get() in self.one_cord:
            self.create_item(self.toolbar.get(), event.x, event.y, **self.get_options())
            self.delete_holo()
            return
        if self.holo_item is None:
            self.curent_coords = [event.x, event.y]
            self.holo_item = self.create[self.toolbar.get()](event.x, event.y, event.x, event.y, **self.get_options())
        elif self.toolbar.get() in self.n_cord:
            self.curent_coords.append(event.x)
            self.curent_coords.append(event.y)
            self.coords(self.holo_item, *self.curent_coords)

    def release(self, event):
        event.x, event.y = self._grid(event.x, event.y)
        if self.toolbar.get() not in self.create:
            return
        if self.toolbar.get() in self.one_cord:
            return
        if self.toolbar.get() not in self.n_cord:
            self.create_item(self.toolbar.get(), *self.curent_coords, event.x, event.y, **self.get_options())
            self.delete(self.holo_item)
            self.holo_item = None

    def press_right(self, event):
        event.x, event.y = self._grid(event.x, event.y)
        if self.toolbar.get() not in self.create:
            return
        if self.holo_item is None:
            return
        if self.toolbar.get() in self.n_cord:
            self.create_item(self.toolbar.get(), *self.curent_coords, event.x, event.y, **self.get_options())
            self.delete(self.holo_item)
            self.holo_item = None

if __name__ == "__main__":
    paint = TkinterPaint()
    paint.mainloop()
