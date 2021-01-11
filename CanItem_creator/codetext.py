import tkinter as tk
import utils

class CodeText(tk.Text):
    """
    Tk Text widget used for creating the canvas code.
    """
    def __init__(self, master, *args, **kwargs):
        self.canvas_name = kwargs.pop("canvas_name", "ca")
        self.canvas_kwargs = kwargs.pop("canvas_kwargs", {})
        super().__init__(master, *args, **kwargs)

        self.is_from_xy = False
        self.from_x = 0
        self.from_y = 0

        self.insert("1.0", "import tkinter\n\n")
        self.insert("3.0", self.canvas_name, "canvas_name")
        self.insert("3.end", " = tkinter.Canvas(")
        
        self.insert("3.end", utils.kwargs_to_str(**self.canvas_kwargs), "canvas_kwargs")
        self.insert("3.end", ")\n")
        self.mark_set("canvas_no_kwargs", "3.end - 1 char") # used in case canvas has no kwargs
        self.insert("4.0", self.canvas_name, "canvas_name")
        self.insert("4.end", ".pack()\n\n\n\n")
        self.mark_set("xy_mark", "5.0")
        self.mark_set("code", "6.0")
        self.insert("7.0", self.canvas_name, "canvas_name")
        self.insert("7.end", ".mainloop()")

        #bind so that tge user can't edit the text:
        self.bind("<KeyPress>", lambda *e: "break")

    def configure_canvas(self, canvas_name=None, **kwargs):
        """
        changes the configuration of canvas in code.
        Use canvas_name kwarg to change the name of the canvas
        """
        if canvas_name is not None:
            self.canvas_name = canvas_name
            self.change_code("canvas_name", canvas_name)
        if kwargs:
            no_kwargs = not self.canvas_kwargs
            self.canvas_kwargs.update(kwargs)
            if no_kwargs:
                self.insert("canvas_no_kwargs", utils.kwargs_to_str(**self.canvas_kwargs), "canvas_kwargs")
            self.change_code("canvas_kwargs", utils.kwargs_to_str(**self.canvas_kwargs))

    def from_xy(self, x, y):
        """
        items should be a dictionary:
            item_id: [coords]
        """
        if self.is_from_xy:
            self.revert_xy()
        self.is_from_xy = True
        self.from_x = x
        self.from_y = y
        self._add_xy(x,y)
        self._update_items_xy(x, y)

    def _update_items_xy(self, x, y):
        for tag in self.tag_names():
            if tag[0] == "i" and tag[-6:] == "coords":
                coords = map(int, self.get_item(tag).split(", "))
                self.change_code(tag, ", ".join(utils.with_x_y(x, y, *coords)))

    def revert_xy(self):
        """
        reverts all items from being scaled with x y.
        """
        self.is_from_xy = False
        self._revert_items_xy()
        self._delete_xy()

    def _revert_items_xy(self):
        for tag in self.tag_names():
            if tag[0] == "i" and tag[-6:] == "coords":
                coords = self.get_item(tag).split(", ")
                self.change_code(tag, ", ".join(map(str, utils.revert_x_y(self.from_x, self.from_y, *coords))))

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
        """
        Adds canvas item to code.
        id_ should beggin with "i"
        """
        self.insert("code", self.canvas_name, (f"{id_}", "canvas_name"))
        self.insert("code", f".create_{name}(", f"{id_}")
        #insert coords
        i = 1
        cord_type = "y"
        self.insert("code", f"{args[0]}", (f"{id_}", f"{id_}coords"))#(f"{id_}x1"))
        for arg in args[1:]:
            self.insert("code", f", {arg}", (f"{id_}", f"{id_}coords"))#(f"{id_}{cord_type}{i}"))
            if cord_type == "x":
                cord_type = "y"
            else:
                cord_type = "x"
                i += 1
        #insert kwargs
        for key, value in kwargs.items():
            self.insert("code", f", {key}={repr(value)}", (f"{id_}{key}", f"{id_}"))
        self.insert("code", f")\n", f"{id_}")

        if self.is_from_xy:
            self.change_code(f"{id_}coords", ", ".join(utils.with_x_y(self.from_x, self.from_y, *args)))

    def remove_code(self):
        """
        removes last line of code
        """
        self.delete("code -1 line", "code")

    #def simple_code_build(self, canvas):
    #    self. build_code(canvas, self.canvas_name, self.canvas_kwargs)

    def get_item(self, id_):
        """
        Retrieves code with item id_.
        if you just want cords put "cords" behind id_
        """
        return self.get(f"{id_}.first", f"{id_}.last")

    def remove_item(self, id_):
        """
        removes the item with id_ from code
        """
        self.delete(f"{id_}.first", f"{id_}.last")
        self._clean_tags()
    
    def _clean_tags(self):
        """
        removes all tags with no tagged characters
        """
        for tag in self.tag_names():
            if not self.tag_ranges(tag):
                self.tag_delete(tag)

    def change_code(self, tag, new):
        """
        changes the tagged code.
        tags are:
        - id_ of item
        - {id_ of item}coords
        - canvas_name
        - canvas_kwargs
        """
        for tag_i in self.tag_ranges(tag)[0::2]:
            tag_range = self.tag_nextrange(tag, tag_i)
            if not tag_range:
                continue
            #this can couse errors when the text has tags on just parts of the text
            #but it will work of now
            tags = self.tag_names(tag_range[0])
            self.replace(tag_range[0], tag_range[1], new, tags)
        #self.replace(f"{tag}.first", f"{tag}.last", new, (f"{tag}",))

    def update_theme(self):
        self.configure(background=self.option_get("background", "Text"),
                       foreground=self.option_get("foreground", "Text"))