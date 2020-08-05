init python:
    import copy
    class CharStats(BaseStatsObject):
        STORE_PREFIX = "char_stats"
        STAT_DEFAULTS = {
            'img' : 'player',
            'atk' : 5,
            'dfn' : 0,
            'lvl' : 1,
            'exp' : 0,
            'hpmax' : 60,
            'hp' : 60,
            'mpmax' : 100,
            'mp' : 100,
            'skills' : [],
            'equip' : {'hand': None, 'head': None, 'chest': None, 'accs': None},
            'turn' : False,
            'defending' : False,
            'condition' : {'burn': False, 'freeze': False, 'paral': False, 'poison': False, 'sleep': False, 'stun': False, 'confus': False, 'wound': False, 'rage': False},
            'dead' : False,
            'bonus_atk' : 0,
            'bonus_dfn' : 0,
            'img_pos' : 0,
            'bar_pos' : 0,
            'dmg_pos' : 0,
        }

        @property
        def hp(self):
            value = self.__dict__['hp']
            if not ( 0 <= value <= self.hpmax ):
                value = max( 0, min( self.hpmax, value ) )
                self.hp = value
            return self.__dict__['hp']
        @property
        def mp(self):
            value = self.__dict__['mp']
            if not ( 0 <= value <= self.mpmax ):
                value = max( 0, min( self.mpmax, value ) )
                self.mp = value
            return self.__dict__['mp']

        def addEquip(self, slot, item):
            if self.equip[slot] == None:
                self.equip[slot] = item
                renpy.say(None, "You equipped {0}.".format(self.equip[slot]))
            else:
                renpy.say(None, "Replacing {0} for {1}.".format(self.equip[slot],item))
        def removeEquip(self, slot, item):
            renpy.say(None, "Removed {0}.".format(self.equip[slot]))
            self.equip[slot] = None



define character.p1 = Character("p1")
default p1 = CharStats("p1")
define character.p2 = Character("p2")
default p2 = CharStats("p2")

define character.a = Character("[name]", image="player")
default a = CharStats("a", img="player", skills=[], equip={'hand': "Bow", 'head': None, 'chest': None, 'accs': None})

define character.y = Character("Yu", image="yu")
default y = CharStats("y", lvl=3, hpmax=102, img="yu", skills=[], equip={'hand': None, 'head': None, 'chest': None, 'accs': None})

define character.c = Character("Chie", image="chie")
default c = CharStats("c", lvl=4, hpmax=110, img="chie", skills=[], equip={'hand': None, 'head': None, 'chest': None, 'accs': None})

define character.f = Character("Fuuka", image="fuuka")
default f = CharStats("f", lvl=5, hpmax=90, img="fuuka", skills=[], equip={'hand': None, 'head': None, 'chest': None, 'accs': None})

define character.r = Character("Rise", image="rise")
default r = CharStats("r", lvl=2, hpmax=130, img="rise", skills=[], equip={'hand': None, 'head': None, 'chest': None, 'accs': None})

# define character.var = Character("Name", image="")
# default var = CharStats("var", img="", skills=[], equip={'hand': None, 'head': None, 'chest': None, 'accs': None})
