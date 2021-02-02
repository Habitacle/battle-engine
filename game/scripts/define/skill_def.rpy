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
            currentplayer._hp += t.finaldmg/2
        if s == souldrain:
            currentplayer._hp += t.finaldmg

    def radarFX(p):
        global skilltext
        global radar_block
        radar_block = False
        if radar in p.p_skills:
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
            if self.type == "active" and not self in char.skills:
                char.skills.append(self)
            if self.type == "passive" and not self in char.p_skills:
                char.p_skills.append(self)

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
