init -10 python:

    class RandomBag(object):
        def __init__(self, choices):
            self.choices = choices
            self.bag = [ ]

        def draw(self):
            if not self.bag:
                self.bag = list(self.choices)
                renpy.random.shuffle(self.bag)
            return self.bag.pop(0)

python early:

    def parse_random(l):

        # Looks for a colon at the end of the line.
        l.require(":")
        l.expect_eol()

        # This is a list of (weight, block) tuples.
        blocks = [ ]

        # ll is a lexer (an object that can match words, numbers, and other parts of text) that accesses the block under the current statement.
        ll = l.subblock_lexer()

        # For each line in the file, check for errors...
        while ll.advance():
            with ll.catch_error():

                # ...determine the weight...
                weight = 1.0

                if ll.keyword('weight'):
                    weight = float(ll.require(ll.float))

                # ...and then store the weight and the statement.
                blocks.append((weight, ll.renpy_statement()))

        return { "blocks" : blocks }

    def next_random(p):

        blocks = p["blocks"]

        # Pick a number between 0 and the total weight.
        total_weight = sum(i[0] for i in blocks)
        n = renpy.random.random() * total_weight

        # Then determine which block that number belongs to.
        for weight, block in blocks:
            if n <= weight:
                break
            else:
                n -= weight

        return block

    renpy.register_statement("random", parse=parse_random, next=next_random, predict_all=True, block=True)

init python:
    class MouseTooltip(renpy.Displayable):

        def __init__(self, **kwargs):
            super(renpy.Displayable, self).__init__(**kwargs)
            self.text = Text("")
            self.textsize = 32
            self.textcolor = Color("#FFF")
            self.padding = 10
            self.bold = True
            self.backgroundcolor = Color("#7777")
            self.x = 0
            self.y = 0

        def render(self, width, height, st, at):
            # avoid to render an empty rectangle when the text got cleared
            if self.text.text != [""]:
                w, h = self.text.size()
                render = renpy.Render(w, h)

                # if tooltip is close to the top or right side make sure it stays on the screen
                x = self.x + self.padding
                if x > config.screen_width - w - self.padding:
                    x = config.screen_width - w - self.padding

                y = self.y-h-self.padding*2 # -h to place text above cursor
                if y < 0:
                    y = 0

                fixed = Fixed(self.backgroundcolor, xpos=-self.padding, xsize=int(w)+self.padding*2, ysize=int(h)+self.padding*2)
                fixed.add(self.text)
                render.place(fixed, x, y)
                return render
            return renpy.Render(1, 1)

        def event(self, ev, x, y, st):
            import pygame
            # ignore all events except MOUSEMOTION
            if ev.type != pygame.MOUSEMOTION:
                return None
            self.x = x
            self.y = y
            tooltip = GetTooltip()
            if tooltip:
                self.text = Text(tooltip, size=self.textsize, color=self.textcolor, xpos=self.padding, ypos=self.padding, bold=self.bold)
                renpy.redraw(self, 0)
            elif self.text.text != [""]: # avoid unnecessary redraw calls
                self.text = Text("") # if there is no tooltip clear the text just once
                renpy.redraw(self, 0)

define mousetooltip = MouseTooltip()

init python:
    class TransitionConditionSwitch(renpy.Displayable):
        def __init__(self, transition, *args, **kwargs):
            super(TransitionConditionSwitch, self).__init__(**kwargs)
            self.transition = transition
            self.d = zip(args[0::2], args[1::2])
            self.time_reset = True
            self.old_d = None
            self.current_d = None
            self.ta = None
        def render(self, width, height, st, at):
            if self.time_reset:
                self.time_reset = False
                self.st = st
                self.at = at
            return renpy.render(self.ta, width, height, st-self.st, at-self.at)
        def per_interact(self):
            change_to = self.current_d
            for name, d in self.d:
                if eval(name):
                    change_to = d
                    break
            if change_to is not self.current_d:
                self.time_reset = True
                self.old_d = self.current_d
                self.current_d = change_to
                if self.old_d is None:
                    self.old_d = self.current_d
                self.ta = anim.TransitionAnimation(self.old_d, 0.00, self.transition, self.current_d)
                renpy.redraw(self, 0)
        def visit(self):
            return [ self.ta ]
