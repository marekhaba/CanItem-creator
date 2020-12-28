import unittest
import tkinter as tk
from context import utils, codetext
#from context import codetext, utils

class TestUtils(unittest.TestCase):

    def test_kwargs_to_str(self):
        self.assertEqual(utils.kwargs_to_str(**{"a": 1, "fill": "red"}), "a=1, fill='red'")

    def test_is_float(self):
        self.assertTrue(utils.is_float("1"))
        self.assertTrue(utils.is_float("-5.1"))
        self.assertFalse(utils.is_float("1as"))

    def test_with_x_y(self):
        self.assertEqual(", ".join(utils.with_x_y(10, 20, *(64, 5, -10, 20, 5))), "x+54, y-15, x-20, y, x-5")
        self.assertEqual(", ".join(map(str, utils.revert_x_y(10, 20, *utils.with_x_y(10, 20, *(64, 5, -10, 20, 5))))), "64, 5, -10, 20, 5")

class TestCodetext(unittest.TestCase):

    def test_canvas_name_config(self):
        master = tk.Tk()
        canvas_name = "can"
        ctext = codetext.CodeText(master, canvas_name=canvas_name, canvas_kwargs={"bg": "black"})
        code = f"""import tkinter\n\n{canvas_name} = tkinter.Canvas(bg='black')\n{canvas_name}.pack()\n\n\n{canvas_name}.mainloop()\n\n"""
        self.assertEqual(ctext.get(1.0, "end"), code)
        canvas_name = "c"
        ctext.configure_canvas(canvas_name=canvas_name)
        code = f"""import tkinter\n\n{canvas_name} = tkinter.Canvas(bg='black')\n{canvas_name}.pack()\n\n\n{canvas_name}.mainloop()\n\n"""
        self.assertEqual(ctext.get(1.0, "end"), code)
        ctext.add_item("i544", "rectangle", *(1, 2, 3, 4), **{"fill": "pink"})
        self.assertEqual(ctext.get_item("i544"), "c.create_rectangle(1, 2, 3, 4, fill='pink')\n")
        ctext.configure_canvas(canvas_name="canvas")
        self.assertEqual(ctext.get_item("i544"), "canvas.create_rectangle(1, 2, 3, 4, fill='pink')\n")
        master.quit()

    def test_canvas_kwargs_config(self):
        master = tk.Tk()
        ctext = codetext.CodeText(master, canvas_name="c", canvas_kwargs={"bg": "black"})
        self.assertEqual(ctext.get("canvas_kwargs.first", "canvas_kwargs.last"), "bg='black'")
        ctext.configure_canvas(bg="blue", width=500)
        self.assertEqual(ctext.get("canvas_kwargs.first", "canvas_kwargs.last"), "bg='blue', width=500")
        master.quit()

    def test_add_item(self):
        master = tk.Tk()
        ctext = codetext.CodeText(master, canvas_name="c")
        ctext.add_item("i123", "rectangle", *(10, 20, -88, 4), **{"fill": "red", "width": 3})
        ctext.add_item("i3", "test", *(10, 2, -8), **{"fi": True, "wih": ["A", "B"]})
        self.assertEqual(ctext.get_item("i123"), "c.create_rectangle(10, 20, -88, 4, fill='red', width=3)\n")
        self.assertEqual(ctext.get_item("i3"), "c.create_test(10, 2, -8, fi=True, wih=['A', 'B'])\n")
        master.quit()
    
    def test_from_revert_xy(self):
        master = tk.Tk()
        ctext = codetext.CodeText(master, canvas_name="c")
        ctext.add_item("i123", "rectangle", *(10, 20, -88, 4), **{"fill": "red", "width": 3})
        ctext.from_xy(10, 15)
        ctext.add_item("i3", "test", *(10, 2, -8), **{"fi": True, "wih": ["A", "B"]})
        self.assertEqual(ctext.get_item("i123"), "c.create_rectangle(x, y+5, x-98, y-11, fill='red', width=3)\n")
        self.assertEqual(ctext.get_item("i3"), "c.create_test(x, y-13, x-18, fi=True, wih=['A', 'B'])\n")
        ctext.from_xy(20, 25)
        self.assertEqual(ctext.get_item("i123"), "c.create_rectangle(x-10, y-5, x-108, y-21, fill='red', width=3)\n")
        self.assertEqual(ctext.get_item("i3"), "c.create_test(x-10, y-23, x-28, fi=True, wih=['A', 'B'])\n")
        ctext.revert_xy()
        self.assertEqual(ctext.get_item("i123"), "c.create_rectangle(10, 20, -88, 4, fill='red', width=3)\n")
        self.assertEqual(ctext.get_item("i3"), "c.create_test(10, 2, -8, fi=True, wih=['A', 'B'])\n")
        master.quit()

if __name__ == "__main__":
    unittest.main()