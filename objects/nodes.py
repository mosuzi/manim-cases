from manimlib import VGroup
from objects.node import Node


class Nodes(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

    def add_node(self, text, *vmobjects, **kwargs):
        node = Node(text, *vmobjects, **kwargs)
        self.add(node)
        return node
