from manimlib import VGroup, Arrow


class Sides(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

    def add_side(self, *args, **kwargs):
        arrow = Arrow(*args, **kwargs)
        self.add(arrow)
        return arrow
