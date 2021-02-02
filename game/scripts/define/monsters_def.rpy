label load_monsters:
    # var = Monster(name, hpmax, atk, dfn, exp, lvl, img, sfx_atk, anim, skills)
    $ empty = Monster(None, None, None, None, None, None, None, None, dead=True)
    $ mon1 = Monster("Lapras", 20, 15, 1.0, 50, 3, "1", "water", anim=slow_sway, skills=[arrowhail])
    $ mon2 = Monster("Ditto", 50, 20, 6.0, 50, 4, "2", "pound", anim=squeeze, skills=[mindfreeze])
    $ mon3 = Monster("Eevee", 30, 40, 3.0, 50, 5, "3", "tackle", anim=idle_shake, skills=[lifedrain])
    $ mon4 = Monster("Vaporeon", 25, 10, 10.0, 50, 4, "4", "water", anim=idle_y, skills=[devastationbeam])
    $ mon5 = Monster("Jolteon", 45, 35, 10.0, 50, 4, "5", "thunder", anim=idle_xy, skills=[asteroid])
    $ mon6 = Monster("Flareon", 70, 50, 9.0, 50, 8, "6", "fire", anim=idle_x, skills=[swordofdeath])
    $ mon7 = Monster("Espeon", 15, 50, 7.0, 50, 5, "7", "cut", anim=idle_shake, skills=[rockthrow])
    $ mon8 = Monster("Umbreon", 55, 25, 2.0, 50, 4, "8", "scratch", anim=idle_shake, skills=[mindburn])
    $ mon9 = Monster("Venasaur", 60, 40, 3.0, 50, 6, "9", "leaf", anim=idle_xy, skills=[lavaburst])
    $ mon10 = Monster("Charizard", 90, 95, 4.0, 50, 8, "10", "fire", anim=idle_shake, skills=[deathmissile])
    $ mon11 = Monster("Blastoise", 85, 85, 5.0, 50, 5, "11", "water", anim=idle_x, skills=[thunderbolt])
    return

init python:
    class Monster(object):
        def __init__(self, name, hpmax, atk, dfn, exp, lvl, img, sfx_atk, anim=idle_shake, skills=[], state=None, dead=False, finaldmg=0, slot=1, sprite_pos=0, dmg_pos=(0,0)):
            self.name = name
            self.hpmax = hpmax
            self._hp = 0
            self._mp = 0
            self.atk = atk
            self.dfn = dfn
            #self.vel = vel
            self.state = state
            self.lvl = lvl
            self.exp = exp
            self.dead = dead
            self.skills = skills
            self.img = img
            self.sfx_atk = sfx_atk
            #self.sfx_cry = sfx_cry
            #self.sfx_die = sfx_die
            self.finaldmg = finaldmg
            self.slot = slot
            self.anim = anim
            self.sprite_pos = sprite_pos
            self.dmg_pos = dmg_pos
            #self.rarity = rarity
        @property
        def hp(self):
            value = self._hp
            if not ( 0 <= value <= self.hpmax ):
                value = max( 0, min( self.hpmax, value ) )
                self._hp = value
            return self._hp
