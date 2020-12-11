import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile 
from optionedits import ColorEdit, IntEdit, StrEdit
from actionmanager import ActionManager

ITEMS = ["line", "rectangle", "oval", "polygon", "arc", "text"]
OPTIONS = {
    "fill": {
        "items": ["line", "rectangle", "oval", "polygon", "arc", "text"],
        "edit": ColorEdit,
        "default": "",
        "kwargs": {"entry_width": 9}},
    "outline": {
        "items": ["rectangle", "oval", "polygon", "arc"],
        "edit": ColorEdit,
        "default": "",
        "kwargs": {"entry_width": 9}},
    "width": {
        "items": ["line", "rectangle", "oval", "polygon", "arc"],
        "edit": IntEdit,
        "default": 1,
        "kwargs": {"entry_width": 3}},
    "text": {
        "items": ["text"],
        "edit": StrEdit,
        "default": "",
        "kwargs": {"entry_width": 10}},
    "anchor": {
        "items": ["text"],
        "edit": StrEdit,
        "default": "center",
        "kwargs": {"entry_width": 3}}
}


def kwargs_to_str(**kwargs):
    return ', '.join('%s=%r' % x for x in kwargs.items())

def args_to_str(*args):
    return ', '.join(map(str, args))

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def options_to_str(options):
    """
    transforms the tkinter options thingy to string
    """
    string = ""
    for option in options.values():
        if is_float(option[3]) and is_float(option[4]):
            if float(option[3]) != float(option[4]):
                string += f", {option[0]} = {option[4]}"
            continue
        if option[3] != option[4]:
            string += f", {option[0]} = {option[4]}"
    return string

def build_code(canvas: tk.Canvas, canvas_name, canvas_config):
    """
    #not really used, replaced with a more fancy way
    will build code that will recreate all items in canvas
    returns a string with that code
    """
    code = "import tkinter\n\n"
    code += f"{canvas_name} = tkinter.Canvas({kwargs_to_str(**canvas_config)})\n"
    code += f"{canvas_name}.pack()\n\n"
    items = canvas.find("all")
    for item in items:
        code += f"{canvas_name}.create_{canvas.type(item)}({args_to_str(canvas.coords(item))}{options_to_str(canvas.itemconfigure(item))})"
    code += f"\n{canvas_name}.mainloop()"
    return code

def with_x_y(x,y, *args):
    is_x = True
    for arg in args:
        if is_x:
            num = int(arg)-x
            if num > 0:
                yield f"x+{num}"
            elif num < 0:
                yield f"x{num}"
            else:
                yield f"x"
            is_x = False
        else:
            num = int(arg)-y
            if num > 0:
                yield f"y+{num}"
            elif num < 0:
                yield f"y{num}"
            else:
                yield f"y"
            is_x = True

class TkinterPaint(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.optionsbar = OptionsBar(self)
        self.optionsbar.grid(row=0, column=1, sticky="w", padx=2, pady=2)

        self.toolbar = ToolBar(self, self.optionsbar)
        self.toolbar.grid(row=1, column=0, sticky="n", padx=2, pady=2)

        self.codetext = CodeText(self, width=100, wrap="none")
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

        self._run_test()

    def change_grid(self, *args):
        self.canvas.set_grid(self.canvas_grid.get())

    def _toggle_grid(self):
        self.canvas.show_grid(self.grid_state.get())

    def toggle_xy(self):
        if self.from_x_y_var.get():
            self.codetext.from_xy(self.canvas.get_items_coords(), self.canvas.from_x, self.canvas.from_y)
            self.from_x_y_btn["state"] = ("!disabled",)
            self.canvas.show_xy()
        else:
            self.codetext.revert_xy(self.canvas.get_items_coords())
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
        self.canvas.configure(**kwargs)
        self.codetext.canvas_config.update(kwargs)

    def _run_test(self):
        assert list(with_x_y(10, 20, 30, 50, 10, 10)) == ["x+20","y+30","x","y-10"]
        #self.codetext.add_item(1, "line", 10, 20, 30, 40, fill="red")
        #assert self.codetext.get("tag1x1.first", "tag1x1.last") == "10"
        #assert self.codetext.get("tag1coords.first", "tag1coords.last") == "10, 20, 30, 40" 


class OptionsBar(ttk.Frame):
    """
    Manages all options for the item
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.edits = {key: ttk.Frame(self) for key in ITEMS}
        for option in OPTIONS:
            for item in OPTIONS[option]["items"]:
                edit = OPTIONS[option]["edit"](self.edits[item], option, **OPTIONS[option]["kwargs"])
                edit.pack(side="left", padx=3, pady=3)

        self.current = None
        #self.fill_edit.show()

    def change_edits(self, name):
        if self.current is not None:
            self.edits[self.current].pack_forget()
        if name not in self.edits:
            self.current = None
            return
        self.edits[name].pack()
        self.current = name

    def get(self):
        """
        returns kwargs of the options.
        """
        if self.current is None:
            return {}
        options = {}
        for edit in self.edits[self.current].winfo_children():
            if edit.get() == OPTIONS[edit.get_name()]["default"]:
                continue
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
        self.tool.trace_add("write", lambda *e: self.optionsbar.change_edits(self.tool.get()))

    def add_tool(self, name: str, image=None):
        """
        Adds tool to the toolbar if image is None, name will be used as label.
        """
        self.tools[name] = ttk.Radiobutton(self, variable=self.tool, value=name, text=name, image=image, style="Toolbutton")
        self.tools[name].pack(side="top", padx=3, pady=3, ipadx=3, ipady=3)

    def get(self):
        return self.tool.get()

    def set_tool(self, tool):
        """
        Sets the curent tool to the passed tool
        """
        self.tool.set(tool)

class CodeText(tk.Text):
    """
    Tk Text widget used for creating the canvas code.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.canvas_name = "ca"
        self.canvas_config = {}

        self.is_from_xy = False
        self.from_x = 0
        self.from_y = 0


        self.insert("1.0", "import tkinter\n\n")
        self.insert("3.0", f"{self.canvas_name} = tkinter.Canvas({kwargs_to_str(**self.canvas_config)})\n")
        self.insert("4.0", f"{self.canvas_name}.pack()\n\n\n\n")
        self.mark_set("xy_mark", "5.0")
        self.mark_set("code", "6.0")
        
        self.insert("7.0", f"{self.canvas_name}.mainloop()")

        #do the editable stuff
        self.bind("<KeyPress>", lambda *e: "break")
        #self.bind("<KeyRelease>", lambda *e: "break")

        #self.insert("code", "abcd")
        #self.insert("code", "efgh\n")
        #self.insert("code", "skapem")
        #self["state"] = "disabled"
        
    # def _add_code(self, canvas):
    #     """
    #     just dumps the whole code string.
    #     nothing fancy
    #     """
    #     self.replace("1.0", "end -2 chars", build_code(canvas, self.canvas_name, self.canvas_config))

    def add_code(self, text, tag):
        """
        appends line of code specified in text,
        specify the name of item in tag
        """
        self.insert("code", text, f"tag{tag}")

    def from_xy(self, items, x, y):
        """
        items should be a dictionary:
            item_id: [coords]
        """
        self.is_from_xy = True
        self.from_x = x
        self.from_y = y
        self._add_xy(x,y)
        self._update_items_xy(items, x, y)

    def revert_xy(self, items):
        self.is_from_xy = False
        self._revert_items_xy(items)
        self._delete_xy()

    def _update_items_xy(self, items, x, y):
        """
        items should be a dictionary:
            item_id: [coords]
        """
        for item, coords in items.items():
            self.change_code(f"{item}coords", ", ".join(with_x_y(x, y, *coords)))

    def _revert_items_xy(self, items):
        for item, coords in items.items():
            self.change_code(f"{item}coords", ", ".join(map(str, coords)))

    def _add_xy(self, x, y):
        self._delete_xy()
        self.insert("xy_mark", f"\nx = {x}", ("xy",))
        self.insert("xy_mark", f"\ny = {y}\n", ("xy",))

    def _delete_xy(self):
        try:
            self.delete("xy.first", "xy.last")
        except tk.TclError:
            return

    def add_item(self, id_, name, *args, **kwargs):
        #mby will continue this in the future sofar deprecated
        self.insert("code", f"{self.canvas_name}.create_{name}(", f"tag{id_}")
        #insert coords
        i = 1
        cord_type = "y"
        self.insert("code", f"{args[0]}", (f"tag{id_}", f"tag{id_}coords"))#(f"tag{id_}x1"))
        for arg in args[1:]:
            self.insert("code", f", {arg}", (f"tag{id_}", f"tag{id_}coords"))#(f"tag{id_}{cord_type}{i}"))
            if cord_type == "x":
                cord_type = "y"
            else:
                cord_type = "x"
                i += 1
        #insert kwargs
        for key, value in kwargs.items():
            if isinstance(value, str):
                self.insert("code", f''', {key}="{value}"''', (f"tag{id_}{key}", f"tag{id_}"))
                continue
            self.insert("code", f", {key}={value}", (f"tag{id_}{key}", f"tag{id_}"))
        self.insert("code", f")\n", f"tag{id_}")
        if self.is_from_xy:
            self.change_code(f"{id_}coords", ", ".join(with_x_y(self.from_x, self.from_y, *args)))

    def remove_code(self):
        """
        removes last line of code
        """
        self.delete("code -1 line", "code")

    #def simple_code_build(self, canvas):
    #    self. build_code(canvas, self.canvas_name, self.canvas_config)

    def remove_item(self, id_):
        """
        removes the item with id_ from code
        """
        self.delete(f"tag{id_}.first", "tag{tag}.last")

    def dump_tag(self, tag):
        """
        quicker way of dumping contents of a tag
        """
        return self.dump(f"tag{tag}.first", f"tag{tag}.last")

    def change_code(self, tag, new):
        """
        changes the tagged code.
        tags are:
        - name of item
        - {name of item}coords
        """
        self.replace(f"tag{tag}.first", f"tag{tag}.last", new, (f"tag{tag}",))
        #TODO remove when finished
        assert self.get(f"tag{tag}.first", f"tag{tag}.last") == new

class PaintCanvas(tk.Canvas):
    """
    tk.Canvas where you can paint stuff,
    """

    def __init__(self, master, toolbar: ToolBar, optionsbar: OptionsBar, codetext: CodeText, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.toolbar = toolbar
        self.toolbar.tool.trace_add("write", self.delete_holo)
        self.optionsbar = optionsbar
        self.optionsbar.bind("<FocusOut>", self.delete_holo, True)
        self.codetext = codetext
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

        self.items = set()#keeps all the <_id>s of items (in reallity they are tags I use them as an _id)
        self.holo_item = None

        self.bind("<Button-1>", self.press)
        self.bind("<Motion>", self.motion)
        self.bind("<ButtonRelease-1>", self.release)
        self.bind("<Button-3>", self.press_right)

        self.canvas_name = "ca"
        
        #used in the functionality that allows scalling from xy
        self.from_x = 0
        self.from_y = 0

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
        #test
        #self.itemconfigure(item)
        #self.codetext.add_code(self)
        #self.codetext.add_code(f"{self.canvas_name}.create_{name}({args_to_str(*args)}, {kwargs_to_str(**kwargs)})\n", item)
        self.codetext.add_item(_id, name, *args, **kwargs)
        #self.code.append(f"{self.canvas_name}.create_{name}({args_to_str(*args)}, {kwargs_to_str(**kwargs)})")
        return _id

    def _delete_item(self, item):
        """
        removes the item\n
        also removes from code
        """
        self.codetext.remove_code()
        self.items.remove(item)
        #self.code.pop()
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
                self.holo_item = self.create[self.toolbar.get()](event.x, event.y, **self.optionsbar.get())
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
            self.create_item(self.toolbar.get(), event.x, event.y, **self.optionsbar.get())
            self.delete_holo()
            return
        if self.holo_item is None:
            self.curent_coords = [event.x, event.y]
            self.holo_item = self.create[self.toolbar.get()](event.x, event.y, event.x, event.y, **self.optionsbar.get())
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
            self.create_item(self.toolbar.get(), *self.curent_coords, event.x, event.y, **self.optionsbar.get())
            self.delete(self.holo_item)
            self.holo_item = None

    def press_right(self, event):
        event.x, event.y = self._grid(event.x, event.y)
        if self.toolbar.get() not in self.create:
            return
        if self.holo_item is None:
            return
        if self.toolbar.get() in self.n_cord:
            self.create_item(self.toolbar.get(), *self.curent_coords, event.x, event.y, **self.optionsbar.get())
            self.delete(self.holo_item)
            self.holo_item = None

if __name__ == "__main__":
    paint = TkinterPaint()
    paint.mainloop()
