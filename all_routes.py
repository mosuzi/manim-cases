from manimlib import *
import sys

sys.path.append(".")
from objects.stack import Stack
from objects.graph import Graph
from objects.stack_obj import StackObj


class GetAllRoutes(Scene):
    def construct(self):
        self.routes = []
        self.result = None
        self.author = Text("bilibili 昭义镇海节度使", font="Microsoft YaHei", font_size=24)
        self.author.shift(BOTTOM * 0.25)
        title = Text(
            "一种简单的有向无环图路径遍历算法", font="Microsoft YaHei", t2c={"有向无环图": YELLOW_E}
        )
        title.shift(UP * 0.25)
        self.play(*[Write(title), FadeIn(self.author)])
        self.wait(1)
        self.play(
            *[
                Uncreate(title),
                self.author.animate.shift(RIGHT_SIDE + TOP + [-1.4, 0.5, 0]),
            ]
        )
        self.save_state()
        self.simple()

        self.clear()
        self.restore()
        node_list = [
            {"name": "1", "position": [0, 2, 0], "color": RED_E},
            {"name": "2", "position": [-1, 1, 0], "color": BLUE_E},
            {"name": "3", "position": [1, 1, 0], "color": YELLOW_E},
            {"name": "4", "position": [-1, -1, 0], "color": GREEN_E},
            {"name": "5", "position": [0, 0, 0], "color": TEAL_E},
            {"name": "6", "position": [1, 0, 0], "color": MAROON_E},
            {"name": "7", "position": [1, -1, 0], "color": GOLD_E},
            {"name": "8", "position": [0, -2, 0], "color": ORANGE},
        ]
        side_list = [
            [0, 4],
            [0, 2],
            [0, 1],
            [1, 4],
            [1, 3],
            [2, 5],
            [3, 7],
            [4, 7],
            [4, 6],
            [4, 5],
            [4, 3],
            [5, 6],
            [6, 7],
        ]
        self.complex_scene(node_list, side_list)
        self.clear()
        self.restore()
        thanks = Text('谢谢观看！', font="Microsoft YaHei",
                      t2g={'[:-1]': (BLUE, GREEN)})
        thanks.shift(UP * 0.15)
        self.play(*[Write(thanks), self.author.animate.shift(-RIGHT_SIDE -
                  TOP * 0.85 - [-1.4, 0.5, 0])])

    def simple(self):
        # draw graph
        graph = Graph()
        node_list = [
            {"name": "1", "position": [0, 1, 0], "color": RED_E},
            {"name": "2", "position": [-0.5, 0, 0], "color": BLUE_E},
            {"name": "3", "position": [0.5, 0, 0], "color": YELLOW_E},
            {"name": "4", "position": [0, -1, 0], "color": GREEN_E},
        ]
        nodes = [
            graph.add_node(
                text=item["name"], color=item["color"], arc_center=item["position"]
            )
            for item in node_list
        ]
        side_list = [[0, 1], [0, 2], [1, 3], [2, 3]]
        sides = [
            graph.add_side(
                nodes[item[0]].get_arc_center()[0], nodes[item[1]].get_arc_center()[0]
            )
            for item in side_list
        ]
        for side in sides:
            side.set_length(side.get_length() - 0.3)
        self.play(Write(graph))
        steps = [
            {"sideIndex": 0, "color": RED_C},
            {"sideIndex": 2, "color": RED_C},
            {"sideIndex": 2, "color": GREEN_C},
            {"sideIndex": 0, "color": GREEN_C},
            {"sideIndex": 1, "color": RED_C},
            {"sideIndex": 3, "color": RED_C},
            {"sideIndex": 3, "color": GREEN_C},
            {"sideIndex": 1, "color": GREEN_C},
        ]
        for step in steps:
            self.wait(1)
            sides[step["sideIndex"]].set_color(step["color"])

        self.wait(1)
        self.play(graph.animate.shift([-4, 0, 0]))

        # draw stacks
        forks = Stack([0, -1, 0], "forks")
        self.play(Write(forks))
        output = Stack([2, -1, 0], "output")
        self.wait(1)
        self.play(Write(output))
        current = Stack([4, -1, 0], "current")
        self.wait(1)
        self.play(Write(current))
        self.wait(1)

        for side in sides:
            side.set_color(WHITE)

        output.push(node_list[0]["name"], self)
        self.wait(0.5)
        current.push(node_list[1]["name"], self)
        current.push(node_list[2]["name"], self)
        self.wait(1)
        forks.push(node_list[0]["name"], self)
        self.wait(1)

        transfer = current.pop(self)
        output.push(transfer.get_text(), self)
        sides[1].set_color(RED_C)
        self.wait(1)

        current.push(node_list[3]["name"], self)
        transfer = current.pop(self)
        output.push(transfer.get_text(), self)
        sides[3].set_color(RED_C)
        self.wait(1)

        # draw result
        result = Text("result: [[1, 3, 4]]", font_size=24, color=YELLOW_C)
        result.shift([0, -2, 0])
        self.play(Write(result))
        self.wait(2)

        output.pop(self)
        sides[3].set_color(GREEN_C)
        output.pop(self)
        sides[1].set_color(GREEN_C)
        forks.pop(self)
        self.wait(1)

        transfer: StackObj = current.pop(self)
        output.push(transfer.get_text(), self)
        sides[0].set_color(RED_C)
        self.wait(1)

        current.push(node_list[3]["name"], self)
        transfer = current.pop(self)
        output.push(transfer.get_text(), self)
        sides[2].set_color(RED_C)
        self.wait(1)

        new_result = Text(
            "result: [[1, 3, 4], [1, 2, 4]]", font_size=24, color=YELLOW_C
        )
        new_result.shift([0, -2, 0])
        self.play(ReplacementTransform(result, new_result))
        self.wait(2)

        output.pop(self)
        sides[2].set_color(GREEN_C)
        output.pop(self)
        sides[0].set_color(GREEN_C)
        self.wait(0.5)
        output.pop(self)

        self.wait(2)

    @staticmethod
    def get_last_index(name, node_list):
        for i in range(len(node_list)):
            if name == node_list[i]["name"]:
                return i
        return

    @staticmethod
    def get_children(index, side_list, node_list):
        result = []
        for i in range(len(side_list)):
            if side_list[i][0] == index:
                result.append(node_list[side_list[i][1]])
        return result

    def draw_result(self, route):
        if self.routes:
            self.routes.append(route)
        else:
            self.routes = [route]
        result = Text(
            "result: [" + ",\n\t\t ".join(str(i) for i in self.routes) + "]",
            font_size=24,
            color=YELLOW_C,
        )
        result.shift(DOWN + [result.get_width() / 2, -result.get_height() / 2, 0])
        if self.result:
            self.play(Transform(self.result, result))
        else:
            self.result = result
            self.play(Write(self.result))
        self.wait(2)

    def complex_scene(self, node_list, side_list):
        self.play(FadeIn(self.author))
        graph = Graph()
        nodes = [
            graph.add_node(
                text=item["name"], color=item["color"], arc_center=item["position"]
            )
            for item in node_list
        ]
        sides = [
            graph.add_side(
                nodes[item[0]].get_arc_center()[0], nodes[item[1]].get_arc_center()[0]
            )
            for item in side_list
        ]
        for side in sides:
            side.set_length(side.get_length() - 0.3)
        self.play(Write(graph))

        self.wait(1)
        self.play(graph.animate.shift([-4, 0, 0]))

        # draw stacks
        forks = Stack([0, 0, 0], "forks")
        self.play(Write(forks))
        output = Stack([2, 0, 0], "output")
        self.wait(1)
        self.play(Write(output))
        current = Stack([4, 0, 0], "current")
        self.wait(1)
        self.play(Write(current))
        self.wait(1)

        output.push(node_list[0]["name"], self, color=node_list[0]["color"])

        # auto run
        has_no_children = False
        while output.get_length():
            next_obj = output.get_stack()[-1]
            next_str = next_obj.get_text()
            next_index = self.get_last_index(next_str, node_list)
            if has_no_children:
                has_no_children = False
                self.draw_result([int(item.get_text()) for item in output.get_stack()])
                while output.get_length() and (
                    forks.get_length() <= 0
                    or output.get_stack()[-1].get_text()
                    != forks.get_stack()[-1].get_text()
                ):
                    output.pop(self)
                    self.wait(1)
                if forks.get_length():
                    forks.pop(self)
                    self.wait(1)
            else:
                children = self.get_children(next_index, side_list, node_list)
                if len(children):
                    for i in range(len(children)):
                        current.push(
                            children[i]["name"], self, color=children[i]["color"]
                        )
                        self.wait(1)
                        if i:
                            forks.push(next_str, self, color=next_obj.get_color())
                            self.wait(1)
                else:
                    has_no_children = True
                    continue
            if current.get_length():
                transfer = current.pop(self)
                output.push(transfer.get_text(), self, color=transfer.get_color())
                self.wait(1)
