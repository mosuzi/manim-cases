from manimlib import VGroup
from objects.sides import Sides
from objects.nodes import Nodes


class Graph(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        self.sides = Sides()
        self.nodes = Nodes()
        super().__init__(self.sides, self.nodes, **kwargs)

    def add_node(self, text, *vmobjects, **kwargs):
        return self.nodes.add_node(text, *vmobjects, **kwargs)

    def add_side(self, *args, **kwargs):
        return self.sides.add_side(*args, **kwargs)
    def get_sides(self):
        return self.sides
