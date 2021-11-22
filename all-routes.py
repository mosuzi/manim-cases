from manimlib import *


class StackObj(Rectangle):
    CONFIG = {
        "fill_opacity": 1,
        "color": RED_E
    }

    def __init__(self, width, height, text="", *vmobjects, **kwargs):
        super().__init__(width, height, *vmobjects, **kwargs)
        textObj = Text(text, font_size=20).shift(self.get_center())
        self.add(textObj)

    def getText(self):
        return self.submobjects[0].text


class Stack(VGroup):
    def __init__(self, position=ORIGIN, text="", **kwargs):
        self.position = position
        self.bottomLen = RIGHT * 0.7
        self.wallHeight = UP * 2
        self.objHeight = 0.3
        bottomEnd = position + self.bottomLen
        leftSide = Line(position, self.wallHeight + position)
        bottom = Line(position, self.bottomLen + position)
        rightSide = Line(bottomEnd, bottomEnd + self.wallHeight)
        text = self.pinText(text)
        super().__init__(leftSide, bottom, rightSide, text, **kwargs)
        self.stack = []

    def pinText(self, text):
        text = Text(text, font_size=28)
        text.next_to(self.position + RIGHT * 0.35, BOTTOM * 0.1)
        return text

    def updateText(self, text, scene: Scene):
        text = self.pinText(text)
        scene.play(ReplacementTransform(self.submobjects[-1], text))
        self.remove(self.submobjects[-1])
        self.add(text)
        return text

    def push(self, objName, scene: Scene, *vmobjects, **kwargs):
        content = StackObj(self.bottomLen[0], self.objHeight, objName, *vmobjects, **kwargs).shift(
            self.position + self.wallHeight - [.0, self.objHeight / 2, .0] + self.bottomLen / 2)
        scene.play(FadeIn(content, run_time=0.4))
        scene.wait(0.5)
        scene.play(content.animate.shift(-self.wallHeight +
                   [.0, self.objHeight * (len(self.stack) + 1), .0]))
        self.stack.append(content)

    def pop(self, scene: Scene):
        content = self.stack.pop()
        scene.play(content.animate.shift(self.wallHeight -
                   [.0, self.objHeight * (len(self.stack) + 1), .0]))
        scene.play(FadeOut(content, run_time=0.4))
        return content

    def doShift(self, position, scene: Scene):
        animates = [item.animate.shift(position) for item in self.stack]
        scene.play(self.animate.shift(position), *animates)

    def getLength(self):
        return len(self.stack)

    def getStack(self):
        return self.stack

    def fadeOut(self, scene):
        # todo: remove all objs in stack
        pass


class Sides(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

    def addSide(self, *args, **kwargs):
        arrow = Arrow(*args, **kwargs)
        self.add(arrow)
        return arrow


class Node(Circle):
    CONFIG = {
        "radius": .3,
        "color": RED_E,
        "fill_opacity": 1.0,
    }

    def __init__(self, text="", *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        textObj = Text(text, font_size=28).shift(self.get_center())
        self.add(textObj)

    def getText(self):
        return self.submobjects[-1].text


class Nodes(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

    def addNode(self, text, *vmobjects, **kwargs):
        node = Node(text, *vmobjects, **kwargs)
        self.add(node)
        return node


class Graph(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        self.sides = Sides()
        self.nodes = Nodes()
        super().__init__(self.sides, self.nodes, **kwargs)

    def addNode(self, text, *vmobjects, **kwargs):
        return self.nodes.addNode(text, *vmobjects, **kwargs)

    def addSide(self, *args, **kwargs):
        return self.sides.addSide(*args, **kwargs)


class GetAllRoutes(Scene):
    def construct(self):
        self.simple()
        self.complexScene()

    def simple(self):
        # draw graph
        graph = Graph()
        nodeList = [{'name': '1', 'position': [0, 1, 0], 'color': RED_E},
                    {'name': '2', 'position': [-0.5, 0, 0], 'color': BLUE_E},
                    {'name': '3', 'position': [0.5, 0, 0], 'color': YELLOW_E},
                    {'name': '4', 'position': [0, -1, 0], 'color': GREEN_E}]
        nodes = [graph.addNode(text=item['name'], color=item['color'],
                               arc_center=item['position']) for item in nodeList]
        sideList = [[0, 1], [0, 2], [1, 3], [2, 3]]
        sides = [graph.addSide(nodes[item[0]].get_arc_center()[0],
                               nodes[item[1]].get_arc_center()[0]) for item in sideList]
        for side in sides:
            side.set_length(side.get_length() - 0.3)
        self.play(Write(graph))
        steps = [{'sideIndex': 0, 'color': RED_C},
                 {'sideIndex': 2, 'color': RED_C},
                 {'sideIndex': 2, 'color': GREEN_C},
                 {'sideIndex': 0, 'color': GREEN_C},
                 {'sideIndex': 1, 'color': RED_C},
                 {'sideIndex': 3, 'color': RED_C},
                 {'sideIndex': 3, 'color': GREEN_C},
                 {'sideIndex': 1, 'color': GREEN_C}]
        for step in steps:
            self.wait(1)
            sides[step['sideIndex']].set_color(step['color'])

        self.wait(1)
        self.play(graph.animate.shift([-4, 0, 0]))

        # draw stacks
        forks = Stack([0, -1, 0], 'forks')
        self.play(Write(forks))
        output = Stack([2, -1, 0], 'output')
        self.wait(1)
        self.play(Write(output))
        current = Stack([4, -1, 0], 'current')
        self.wait(1)
        self.play(Write(current))
        self.wait(1)

        for side in sides:
            side.set_color(WHITE)

        output.push(nodeList[0]['name'], self)
        self.wait(0.5)
        current.push(nodeList[1]['name'], self)
        current.push(nodeList[2]['name'], self)
        self.wait(1)
        forks.push(nodeList[0]['name'], self)
        self.wait(1)

        transfer = current.pop(self)
        output.push(transfer.getText(), self)
        sides[1].set_color(RED_C)
        self.wait(1)

        current.push(nodeList[3]['name'], self)
        transfer = current.pop(self)
        output.push(transfer.getText(), self)
        sides[3].set_color(RED_C)
        self.wait(1)

        # draw result
        result = Text('result: [[1, 3, 4]]', font_size=24, color=YELLOW_C)
        result.shift([0, -2, 0])
        self.play(Write(result))
        self.wait(2)

        output.pop(self)
        sides[3].set_color(GREEN_C)
        output.pop(self)
        sides[1].set_color(GREEN_C)
        forks.pop(self)
        self.wait(1)

        transfer = current.pop(self)
        output.push(transfer.getText(), self)
        sides[0].set_color(RED_C)
        self.wait(1)

        current.push(nodeList[3]['name'], self)
        transfer = current.pop(self)
        output.push(transfer.getText(), self)
        sides[2].set_color(RED_C)
        self.wait(1)

        newResult = Text('result: [[1, 3, 4], [1, 2, 4]]',
                         font_size=24, color=YELLOW_C)
        newResult.shift([0, -2, 0])
        self.play(ReplacementTransform(result, newResult))
        self.wait(2)

        output.pop(self)
        sides[2].set_color(GREEN_C)
        output.pop(self)
        sides[0].set_color(GREEN_C)
        self.wait(0.5)
        output.pop(self)

        self.wait(2)

    def getLastIndex(self, name, nodeList):
        for i in range(len(nodeList)):
            if (name == nodeList[i]['name']):
                return i
        return

    def getChildren(self, index, sideList, nodeList):
        result = []
        for i in range(len(sideList)):
            if sideList[i][0] == index:
                result.append(nodeList[sideList[i][1]])
        return result

    def drawResult(self, route):
        if self.routes:
            self.routes.append(route)
        else:
            self.routes = [route]
        result = Text(
            'result: [' + ",\n\t\t ".join(str(i) for i in self.routes) + ']', font_size=24, color=YELLOW_C)
        result.next_to([-1, -2, 0])
        if self.result:
            self.play(Transform(self.result, result))
        else:
            self.result = result
            self.play(Write(self.result))
        self.wait(2)

    def complexScene(self):
        self.result = None
        self.routes = []
        self.clear()
        nodeList = [{'name': '1', 'position': [0, 2, 0], 'color': RED_E},
                    {'name': '2', 'position': [-1, 1, 0], 'color': BLUE_E},
                    {'name': '3', 'position': [1, 1, 0], 'color': YELLOW_E},
                    {'name': '4', 'position': [-1, -1, 0], 'color': GREEN_E},
                    {'name': '5', 'position': [0, 0, 0], 'color': TEAL_E},
                    {'name': '6', 'position': [1, 0, 0], 'color': MAROON_E},
                    {'name': '7', 'position': [1, -1, 0], 'color': GOLD_E},
                    {'name': '8', 'position': [0, -2, 0], 'color': ORANGE}]
        sideList = [[0, 4], [0, 2], [0, 1], [1, 4], [
            1, 3], [2, 5], [3, 7], [4, 5], [5, 6], [6, 7]]
        graph = Graph()
        nodes = [graph.addNode(text=item['name'], color=item['color'],
                               arc_center=item['position']) for item in nodeList]
        sides = [graph.addSide(nodes[item[0]].get_arc_center()[0],
                               nodes[item[1]].get_arc_center()[0]) for item in sideList]
        for side in sides:
            side.set_length(side.get_length() - 0.3)
        self.play(Write(graph))

        self.wait(1)
        self.play(graph.animate.shift([-4, 0, 0]))

        # draw stacks
        forks = Stack([0, 0, 0], 'forks')
        self.play(Write(forks))
        output = Stack([2, 0, 0], 'output')
        self.wait(1)
        self.play(Write(output))
        current = Stack([4, 0, 0], 'current')
        self.wait(1)
        self.play(Write(current))
        self.wait(1)

        output.push(nodeList[0]['name'], self, color=nodeList[0]['color'])

        # auto run
        hasNoChildren = False
        while output.getLength():
            next = output.getStack()[-1]
            nextStr = next.getText()
            nextIndex = self.getLastIndex(nextStr, nodeList)
            if hasNoChildren:
                hasNoChildren = False
                self.drawResult([int(item.getText())
                                for item in output.getStack()])
                while output.getLength() and (forks.getLength() <= 0 or output.getStack()[-1].getText() != forks.getStack()[-1].getText()):
                    output.pop(self)
                    self.wait(1)
                if forks.getLength():
                    forks.pop(self)
                    self.wait(1)
            else:
                children = self.getChildren(nextIndex, sideList, nodeList)
                if len(children):
                    for i in range(len(children)):
                        current.push(
                            children[i]['name'], self, color=children[i]['color'])
                        self.wait(1)
                        if i:
                            forks.push(nextStr, self, color=next.get_color())
                            self.wait(1)
                else:
                    hasNoChildren = True
                    continue
            if current.getLength():
                transfer = current.pop(self)
                output.push(transfer.getText(), self,
                            color=transfer.get_color())
                self.wait(1)
