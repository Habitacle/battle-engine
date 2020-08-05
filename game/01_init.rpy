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

init -10 python:
    class BaseStatsObject(object):
        """
        Base class for defaulting stats and integrating with the store.

        Designed to be extended by just overloading the constants


        Example of extended class

        class EnemyStats(BaseStatsObject):

            # Set the store.{prefix}.character_id value
            STORE_PREFIX = "enemy_stats"

            # Boolean toggle for validation - defaults both True
            VALIDATE_VALUES = True
            COERCE_VALUES = False

            STAT_DEFAULTS = {
                'element' : 'earth',
                'hp' : 50,
                'mp' : 40,
                'rarity' : 0.075,
            }

        """

        STORE_PREFIX = "character_stats"
        VALIDATE_VALUES = True
        COERCE_VALUES = True

        STAT_DEFAULTS = {}

        def __init__(self, id, **kwargs):
            """
            Initialize values from store or kwargs or default

            @param id: A unique id to use in the store. Generally set to
            the Character reference to allow cross object lookups

            @param **kwargs: Setup values that are not default
            """

            if not isinstance(id, basestring):
                id = str(id) # should raise if not stringable

            self.__dict__['_id'] = id

            self.run_optional_method( '__pre_init__', id, **kwargs )

            store_name = "{prefix}_{suffix}".format(
                prefix = type(self).STORE_PREFIX,
                suffix = self.__dict__['_id'] )

            setattr(store, store_name, {})

            self.__dict__['_store'] = getattr(store, store_name)

            for key, value in self.__dict__['_store']:

                setattr(self, key, value)
            # We use:
                # Store value
                # else kwargs value
                # else default value

            for key, value in kwargs.items():

                if key not in self.__dict__['_store']:

                    setattr(self, key, value)

            for key, value in type(self).STAT_DEFAULTS.items():

                if key not in self.__dict__['_store']:

                    setattr(self, key, value)

            for key in [ k for k in self.__dict__['_store']
                         if k not in self.__dict__ ]:

                self.__dict__[k] = self.__dict__['_store'][k]

            self.run_optional_method( '__post_init__', id, **kwargs )


        def __repr__(self):

            return "\n".join( [
                "{} : {}".format( k, getattr(self, k) )
                for k in self.__dict__['_store']
                if k[0] != '_' ] )


        def run_optional_method(self,
                                method_type='post_init',
                                *args,
                                **kwargs):
            """
            Run a method of the object if it exists
            """
            try:
                getattr( self, self.__dict__[ method_type ] )( *args,
                                                               **kwargs )
            except:
                pass


        def get_validated_value(self, key, value):
            """
            Return a value after validating where applicable
            """

            if not type(self).VALIDATE_VALUES:
                return value

            if not key in self.__dict__:
                return value

            default_type = type( self.__dict__[key] )

            if isinstance(value, default_type):
                return value

            if type(self).COERCE_VALUES:
                try:
                    return default_type(value)
                except:
                    pass

            raise TypeError, "Supplied value '{0}' for key '{1}' does not " \
                             "match the existing '{2}'".format(
                                value,
                                key,
                                default_type)


        def __setattr__(self, key, value):

            value = self.get_validated_value(key, value)

            self.__dict__[key] = value

            # Anything not recognized as an attribute of object
            # is placed into the store

            if key not in dir(object):

                self.__dict__['_store'][key] = value


        def __getattr__(self, key):

            try:

                return self.__dict__['_store'][key]

            except:

                if key in self.__dict__:

                    return self.__dict__[key]

                else:

                    try:

                        # try the character object
                        value = getattr(
                                    getattr( character, self._id ),
                                             key )

                        if key != 'name':

                            return value

                        # substitute the name (for interpolation/translations)
                        return renpy.substitutions.substitute(value)[0]

                    except:

                        pass

            try:

                return super(BaseStatsObject, self).__getattr__(key)

            except:

                return super(BaseStatsObject, self).__getattribute__(key)


        def __getattribute__(self, key):

            # Check if the attribute is an @property first

            v = object.__getattribute__(self, key)

            if hasattr(v, '__get__'):

                return v.__get__(None, self)

            # Try the store if the attribute is not in base object

            if key not in dir(object):

                try:

                    return self.__dict__['_store'][key]

                except:

                    pass

            return super(BaseStatsObject, self).__getattribute__(key)


        def __setstate__(self, data):
            self.__dict__.update(data)


        def __getstate__(self):
            return self.__dict__


        def __delattr__(self, key):
            del self.__dict__[key]
