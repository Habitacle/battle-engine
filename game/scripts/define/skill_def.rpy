label load_skills:
    # ACTIVE SKILLS (name, pwr, mp_cost, sfx, targ, targs, type='active', trans=None, img=None, back_row=False)
    $ doubleattack = ActiveSkill("Double Attack", 25, 5, "sword", "enemy", 2, back_row=True) # two enemy targets
    $ attackall = ActiveSkill("Attack All", 75, 45, "rock", "all") # targets all enemies
    $ magicheal = ActiveSkill("Magic Heal", -50, 25, "heal", "self") # negative pwr to heal
    $ defenseup = ActiveSkill("Defense Up", 0, 25, "defend", "self") # use is in skill_effects
    $ magicswap = ActiveSkill("Magic Swap", 0, 15, "heal", "enemy", 2, back_row=True) # can target back row
    $ arrowhail = ActiveSkill("Arrow Hail", 10, 40, "bow", "all", img="arrowhail", back_row=True)
    $ mindfreeze = ActiveSkill("Mind Freeze", 15, 5, "ice", img="mindfreeze", back_row=True)
    $ thunderbolt = ActiveSkill("Thunderbolt", 35, 10, "thunder", "enemy", 3, img="thunderbolt", back_row=True)
    $ iceball = ActiveSkill("Ice Ball", 30, 5, "ice", "row", img="iceball") # attacks whole row
    $ asteroid = ActiveSkill("Asteroid", 20, 5, "rock", img="asteroid")
    $ swordofdeath = ActiveSkill("Sword of Death", 30, 10, "sword", img="swordofdeath")
    $ rockthrow = ActiveSkill("Rock Throw", 30, 40, "rock", "enemy", 2, back_row=True, img="rockthrow")
    $ spikeshield = ActiveSkill("Spike Shield", 45, 70, "block", "all", img="spikeshield")
    $ circleofhealing = ActiveSkill("Circle of Healing", -30, 10, "heal", "ally", img="circleofhealing")
    $ mindburn = ActiveSkill("Mindburn", 35, 15, "fire", img="mindburn")
    $ mindblast = ActiveSkill("Mindblast", 20, 5, "thunder", img="mindblast")
    $ souldrain = ActiveSkill("Soul Drain", 80, 60, "acid", img="souldrain")
    $ lavaburst = ActiveSkill("Lava Burst", 20, 5, "fire", img="lavaburst")
    $ deathmissile = ActiveSkill("Death Missile", 70, 45, "rock", img="deathmissile")
    $ meteorshower = ActiveSkill("Meteor Shower", 80, 40, "rock", "all", img="meteorshower")
    $ hellrage = ActiveSkill("Hell Rage", 120, 80, "fire", "all", img="hellrage")
    $ lifedrain = ActiveSkill("Life Drain", 80, 15, "acid", img="lifedrain")
    $ devastationbeam = ActiveSkill("Devastation Beam", 30, 5, "fire", "all", img="devastationbeam")
    $ energybeams = ActiveSkill("Energy Beams", 70, 40, "thunder", "all", img="energybeams")
    $ giftofangels = ActiveSkill("Gift of Angels", -35, 10, "heal", "ally", 2, img="giftofangels")

    # PASSIVE SKILLS (name, sfx=None, img=None, trans=None, lvl=0)
    $ radar = PassiveSkill("Radar", "heal")
    $ passive1 = PassiveSkill("Passive Skill 1", "heal")
    $ passive2 = PassiveSkill("Passive Skill 2", "heal")

    # ADD SKILLS TO PLAYERS
    # passive skills
    $ radar.addSkill(y)
    $ passive1.addSkill(a)
    $ passive2.addSkill(c)
    # active skills with imgs
    $ arrowhail.addSkill(a)
    $ mindfreeze.addSkill(a)
    $ thunderbolt.addSkill(a)
    $ iceball.addSkill(f)
    $ lifedrain.addSkill(f)
    $ devastationbeam.addSkill(f)
    $ energybeams.addSkill(f)
    $ giftofangels.addSkill(f)
    $ asteroid.addSkill(r)
    $ swordofdeath.addSkill(r)
    $ rockthrow.addSkill(r)
    $ spikeshield.addSkill(r)
    $ circleofhealing.addSkill(c)
    $ mindburn.addSkill(c)
    $ mindblast.addSkill(c)
    $ souldrain.addSkill(c)
    $ lavaburst.addSkill(y)
    $ deathmissile.addSkill(y)
    $ meteorshower.addSkill(y)
    $ hellrage.addSkill(y)
    # active skills without imgs
    $ attackall.addSkill(a)
    $ doubleattack.addSkill(r)
    $ magicheal.addSkill(a)
    $ defenseup.addSkill(c)
    $ magicswap.addSkill(y)

    return

label skill_effects:
    if b_skill == defenseup:
        $ currentplayer.bonus_dfn += 5
    elif b_skill == magicswap:
        $ skilltext = "SWaP!"
        $ skill_t.append(picked_targs[0])
        $ skill_t.append(picked_targs[1])
        $ swapSlot(monster_slot.index(picked_targs[0]), monster_slot.index(picked_targs[1]))

    return

init python:
    def canTarget(m):
        global currentplayer
        global picked_targs
        if renpy.get_screen("select_monster") and not m in picked_targs:
            # OPTIONAL: must clear all front row first
            # if all(m.dead for m in monster_slot[4:8]):
            #     return True
            if monster_slot.index(m) > 3: # if m is in front row
                return True
            if currentplayer != None:
                if currentplayer.equip['hand'] == "Bow": # if player has bow
                    return True
            if isinstance(b_skill, Skill):
                if b_skill.back_row: # specific skills
                    return True
            if monster_slot[monster_slot.index(m)+4].dead: # if there's no monster blocking it
                return True
        else:
            return False

    def skillChk(p):
        global skill_t
        if radarFX(p):
            return True
        else:
            skill_t.append(p)
            return False

    def afterFX(s, t):
        global currentplayer
        if s == lifedrain:
            currentplayer.hp += t.finaldmg/2
        if s == souldrain:
            currentplayer.hp += t.finaldmg

    def radarFX(p):
        global skilltext
        global radar_block
        radar_block = False
        if radar in p.skills:
            miss_roll = renpy.random.randint(1, 10)
            if miss_roll > 2:
                renpy.play("audio/battle/skills/defend.ogg")
                radar_block = True
                skilltext = "blOcK!"
                renpy.pause(1, hard=True)
                return False
            else:
                return True
        else:
            return True

    def sensIf(s):
        if currentplayer.mp > s.mp_cost:
            if s == magicswap:
                if (monsters_total - monsters_dead) <= 1:
                    return False
            return True
        else:
            return False

    class Skill(object):
        def __init__(self, name, sfx=None, img=None, trans=None, lvl=0, type='active'):
            self.name = name
            self.type = type
            self.sfx = sfx
            self.img = img
            self.trans = trans
            self.lvl = lvl

        def addSkill(self, char):
            if not self in char.skills:
                char.skills.append(self)

        def useSkill(self):
            global damage
            global mp_lost
            global atk_sfx
            global s_trans
            global msg_skill
            damage = self.pwr
            mp_lost = self.mp_cost
            atk_sfx = "audio/battle/skills/" + self.sfx + ".ogg"
            msg_skill = self.name
            s_trans = self.trans

    class PassiveSkill(Skill):
        def __init__(self, name, sfx=None, img=None, trans=None, lvl=0, type='passive'):
            super(Skill, self).__init__()
            self.name = name
            self.type = type
            self.sfx = sfx
            self.img = img
            self.trans = trans
            self.lvl = lvl

    class ActiveSkill(Skill):
        def __init__(self, name, pwr, mp_cost, sfx='sword', targ='enemy', targs=1, type='active', trans=None, img=None, dice=[2,8], acc=0, lvl=0, back_row=False):
            super(Skill, self).__init__()
            self.name = name
            self.pwr = pwr
            self.type = type
            self.mp_cost = mp_cost
            self.sfx = sfx
            self.img = img
            self.trans = trans
            self.targ = targ
            self.targs = targs
            self.dice = dice
            self.acc = acc
            self.lvl = lvl
            self.back_row = back_row
