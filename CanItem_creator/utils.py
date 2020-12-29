"""
Utility functions
"""
def _repr_double(obj):
    """
    Works just like repl but with double qoutes on string
    """
    #not used kept If I want to add this in the future
    string = repr(obj)
    return f'"{string[1:-1]}"' if isinstance(obj, str) else string

def kwargs_to_str(**kwargs):
    return ', '.join(f'{key}={repr(value)}' for key, value in kwargs.items())

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def with_x_y(x, y, *args):
    """
    Scales all args with x, y.
    """
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

def revert_x_y(x, y, *args):
    """
    Reverts with_x_y.
    """
    is_x = True
    for arg in args:
        if is_x:
            is_x = False
            if arg == "x":
                yield x
                continue
            num = x+int(arg[1:])
            yield f"{num}"
        else:
            is_x = True
            if arg == "y":
                yield y
                continue
            num = y+int(arg[1:])
            yield f"{num}"

def remove_default_options(options, defaults):
    """
    options should be regular dictionary
    defaults should be the tkinter widget.configure response
    """
    without_defaults = {}
    for option, value in options.items():
        if is_float(defaults[option][3]):
            if float(value) != float(defaults[option][3]):
                without_defaults[option] = value
            continue
        if value != defaults[option][3]:
            without_defaults[option] = value
    return without_defaults
