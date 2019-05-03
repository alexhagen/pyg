
#from colour.colour import Color as _c

try:
    from colour.colour import Color as _c
except ModuleNotFoundError:
    from colour import Color as _c


class palette(dict):
    def __init__(self, name, screen_policy=False):
        self.name = name
        self.screen_policy = screen_policy

    def add_color(self, name, value, screen=False):
        pass

    def screen(self):
        pass
