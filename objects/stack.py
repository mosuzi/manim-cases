from manimlib import VGroup, ORIGIN, RIGHT, UP, BOTTOM, Line, Text, Scene, ReplacementTransform, FadeIn, FadeOut
from typing import List
from objects.stack_obj import *


class Stack(VGroup):
    def __init__(self, position=ORIGIN, text="", **kwargs):
        self.position = position
        self.bottomLen = RIGHT * 0.7
        self.wallHeight = UP * 2
        self.objHeight = 0.3
        bottom_end = position + self.bottomLen
        left_side = Line(position, self.wallHeight + position)
        bottom = Line(position, self.bottomLen + position)
        right_side = Line(bottom_end, bottom_end + self.wallHeight)
        text = self.pin_text(text)
        super().__init__(left_side, bottom, right_side, text, **kwargs)
        self.stack: List[StackObj] =  []

    def pin_text(self, text):
        text = Text(text, font_size=28)
        text.next_to(self.position + RIGHT * 0.35, BOTTOM * 0.1)
        return text

    def update_text(self, text, scene: Scene):
        text = self.pin_text(text)
        scene.play(ReplacementTransform(self.submobjects[-1], text))
        self.remove(self.submobjects[-1])
        self.add(text)
        return text

    def push(self, obj_name, scene: Scene, *vmobjects, **kwargs):
        content = StackObj(self.bottomLen[0], self.objHeight, obj_name, *vmobjects, **kwargs).shift(
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

    def do_shift(self, position, scene: Scene):
        animates = [item.animate.shift(position) for item in self.stack]
        scene.play(self.animate.shift(position), *animates)

    def get_length(self):
        return len(self.stack)

    def get_stack(self):
        return self.stack

    def fade_out(self, scene):
        # todo: remove all objs in stack
        pass
