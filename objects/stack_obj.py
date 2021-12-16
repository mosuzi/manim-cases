from manimlib import Rectangle, RED_E, Text


class StackObj(Rectangle):
    CONFIG = {
        "fill_opacity": 1,
        "color": RED_E
    }

    def __init__(self, width, height, text="", *vmobjects, **kwargs):
        super().__init__(width, height, *vmobjects, **kwargs)
        text_obj = Text(text, font_size=20).shift(self.get_center())
        self.add(text_obj)

    def get_text(self):
        return self.submobjects[0].text
