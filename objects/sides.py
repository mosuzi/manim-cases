from manimlib import VGroup, Arrow
from objects.node import Node


class Sides(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.sides = []

    def add_side(self, fr: Node , to: Node):
        arrow = Arrow(fr.get_arc_center()[0], to.get_arc_center()[0])
        self.sides.append((fr, to, arrow))
        self.add(arrow)
        return arrow
