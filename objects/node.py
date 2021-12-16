from manimlib import Circle, RED_E, Text


class Node(Circle):
    CONFIG = {
        "radius": .3,
        "color": RED_E,
        "fill_opacity": 1.0,
    }

    def __init__(self, text="", *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        text_obj = Text(text, font_size=28).shift(self.get_center())
        self.add(text_obj)

    def get_text(self):
        return self.submobjects[-1].text
