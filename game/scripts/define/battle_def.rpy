init python:
    def monstersFixed():
        global monsters_total
        global battle_monsters
        global m1
        global m2
        global m3
        global m4
        global m5
        global m6
        global m7
        global m8
        m1 = copy.deepcopy(empty)
        m2 = copy.deepcopy(empty)
        m3 = copy.deepcopy(empty)
        m4 = copy.deepcopy(empty)
        m5 = copy.deepcopy(empty)
        m6 = copy.deepcopy(empty)
        m7 = copy.deepcopy(empty)
        m8 = copy.deepcopy(empty)
        if fixedset == "set 1":
            m2 = copy.deepcopy(mon4)
            m3 = copy.deepcopy(mon5)
            m4 = copy.deepcopy(mon6)
            m5 = copy.deepcopy(mon7)
            m6 = copy.deepcopy(mon8)
            m7 = copy.deepcopy(mon3)
            battle_monsters = [m2,m3,m4,m5,m6,m7]
        else:
            m1 = copy.deepcopy(mon1)
            battle_monsters = [m1]
        monsters_total = len(battle_monsters)
        for m in battle_monsters:
            if m.name:
                m._hp = m.hpmax

    def monstersRoll():
        global monsters_total
        global battle_monsters
        global m1
        global m2
        global m3
        global m4
        global m5
        global m6
        global m7
        global m8
        monsters_total = renpy.random.randint(1,8)
        m1 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m2 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m3 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m4 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m5 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m6 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m7 = copy.deepcopy(renpy.random.choice(wild_monsters))
        m8 = copy.deepcopy(renpy.random.choice(wild_monsters))
        battle_monsters = [m1,m2,m3,m4,m5,m6,m7,m8]
        total = monsters_total
        for m in battle_monsters:
            m._hp = m.hpmax
            m.dead = True
        for m in battle_monsters:
            if total > 0:
                m.dead = False
                total -= 1

    def asignPos():
        monster_slot[0].sprite_pos = 0
        monster_slot[1].sprite_pos = 256
        monster_slot[2].sprite_pos = 512
        monster_slot[3].sprite_pos = 768
        monster_slot[4].sprite_pos = 0
        monster_slot[5].sprite_pos = 256
        monster_slot[6].sprite_pos = 512
        monster_slot[7].sprite_pos = 768
        monster_slot[0].dmg_pos = (576,320)
        monster_slot[1].dmg_pos = (832,320)
        monster_slot[2].dmg_pos = (1088,320)
        monster_slot[3].dmg_pos = (1344,320)
        monster_slot[4].dmg_pos = (576,512)
        monster_slot[5].dmg_pos = (832,512)
        monster_slot[6].dmg_pos = (1088,512)
        monster_slot[7].dmg_pos = (1344,512)

    def swapSlot(old_slot, new_slot):
        renpy.hide_screen("display_monsters")
        monster_slot[old_slot], monster_slot[new_slot] = monster_slot[new_slot], monster_slot[old_slot]
        asignPos()
        renpy.show_screen("display_monsters")

    def partyRevive():
        for c in party_list:
            c.bonus_dfn = 0
            if c.dead == True:
                c.dead = False
                c._hp = 1

    def restorehp():
        for c in party_list:
            c._hp = c.hpmax

    def restoremp():
        for c in party_list:
            c._mp = c.mpmax

    def startPlayersTurn():
        for p in battle_players:
            p.turn = False
            p.defending = False

    def endTurn():
        global currentplayer
        global target
        global hp_lost
        global mp_lost
        global dropitem
        global message
        global misstext
        message = "other_skill"
        misstext = renpy.random.choice(misstext_list)
        if isinstance(b_skill, Skill):
            b_skill.useSkill()
        elif isinstance(b_skill, Item):
            useItem(b_skill)
        if target == "all":
            atkAll()
        if target == "enemy" or target == "row":
            atkEnemy()
        if target == "ally":
            atkAlly()
        if target == "self":
            atkSelf()
        if target == "ko":
            atkAlly()
        if target == "attack":
            Attack()
        if target == "defend":
            message = "defend"
            Defend()
        currentplayer.turn = True
        currentplayer._mp -= mp_lost
        currentplayer._hp -= hp_lost
        player_inv.drop(dropitem)
        renpy.pause(1.5, hard=True)
        playersChk()
        renpy.hide_screen("monster_dmg")

    def startTurn():
        global damage
        global mpdmg
        global mp_lost
        global hp_lost
        global atk_sfx
        global target
        global message
        global picked_targs
        global hit_t
        global missed_t
        global skill_t
        global dropitem
        global row1btn
        global row2btn
        row1btn = False
        row2btn = False
        target = "enemy"
        message = "skill"
        damage = 0
        mpdmg = 0
        mp_lost = 0
        hp_lost = 0
        atk_sfx = None
        dropitem = None
        picked_targs = []
        hit_t = []
        missed_t = []
        skill_t = []

    def playersCnt():
        global players
        global alive_players
        players = 0
        alive_players = []
        for p in battle_players:
            if p.hp > 0:
                p.dead = False
                players += 1
                alive_players.append(p)

    def playersChk():
        global message
        global koplayer
        global battleEnd
        global monsters_dead
        global msg_mons
        global win
        for p in battle_players:
            if p.hp == 0 and not p.dead:
                renpy.pause(0.5)
                p.dead = True
                koplayer = p.name
                message = "player_ko"
                renpy.pause(0.7)
        for m in battle_monsters:
            if m.hp <= 0 and not m.dead:
                m.state = "dying"
                msg_mons = m.name
                message = "m_dead"
                renpy.play(sfx_monsterdead.draw())
                renpy.pause(1)
                message = "none"
                monsters_dead += 1
                m.dead = True
        if all(p.hp == 0 for p in battle_players):
            battleEnd = True
        if monsters_dead == monsters_total:
            message = "you_win"
            win = True
            battleEnd = True

    def getImage(i):
        if isinstance(i, Monster):
            return "images/monsters/"+ i.img+".png"
        if isinstance(i, Skill):
            return "images/skills/" + i.img + ".png"

    def playerAction(p):
        if not battleEnd and not p.turn:
            if renpy.get_screen("turn_select"):
                return Return(p)
            else:
                return NullAction()
        else:
            return NullAction()

    def runEvent():
        global eventrunning
        eventrunning = True
        config.allow_skipping = True
        config.rollback_enabled = True
        renpy.choice_for_skipping()
        renpy.hide_screen("tooltip")
        renpy.retain_after_load()
    def stopEvent():
        global eventrunning
        eventrunning = False
        config.allow_skipping = False
        config.rollback_enabled = False
        renpy.block_rollback()
        renpy.choice_for_skipping()
        preferences.afm_enable = False

default fixedset = None
default tt_timer = False
default damage = 0
default m_damage = 0
default dropitem = None
default atk_sfx = None
default mp_lost = 0
default hp_lost = 0
default players = 1
default monsters_total = 0
default monsters_dead = 0

default b_skill = "none"
default message = "none"
default target = "none"

default picked_targs = []
default party_list = []
default wild_monsters = []
default battle_players = []
default alive_players = []
default battle_monsters = []
default misstext_list = ["MiSs!", "MisS!", "mISs!", "mIsS!"]

default diss = Dissolve(.2)

# ACTIVE SKILLS (name, pwr, mp_cost, sfx, targ, targs, type='active', trans=None, img=None, back_row=False)
default doubleattack = ActiveSkill("Double Attack", 25, 5, "sword", "enemy", 2, back_row=True) # two enemy targets
default attackall = ActiveSkill("Attack All", 75, 45, "rock", "all") # targets all enemies
default magicheal = ActiveSkill("Magic Heal", -50, 25, "heal", "self") # negative pwr to heal
default defenseup = ActiveSkill("Defense Up", 0, 25, "defend", "self") # use is in skill_effects
default magicswap = ActiveSkill("Magic Swap", 0, 15, "heal", "enemy", 2, back_row=True) # can target back row
default arrowhail = ActiveSkill("Arrow Hail", 10, 40, "bow", "all", img="arrowhail", back_row=True)
default mindfreeze = ActiveSkill("Mind Freeze", 15, 5, "ice", img="mindfreeze", back_row=True)
default thunderbolt = ActiveSkill("Thunderbolt", 35, 10, "thunder", "enemy", 3, img="thunderbolt", back_row=True)
default iceball = ActiveSkill("Ice Ball", 30, 5, "ice", "row", img="iceball") # attacks whole row
default asteroid = ActiveSkill("Asteroid", 20, 5, "rock", img="asteroid")
default swordofdeath = ActiveSkill("Sword of Death", 30, 10, "sword", img="swordofdeath")
default rockthrow = ActiveSkill("Rock Throw", 30, 40, "rock", "enemy", 2, back_row=True, img="rockthrow")
default spikeshield = ActiveSkill("Spike Shield", 45, 70, "block", "all", img="spikeshield")
default circleofhealing = ActiveSkill("Circle of Healing", -30, 10, "heal", "ally", img="circleofhealing")
default mindburn = ActiveSkill("Mindburn", 35, 15, "fire", img="mindburn")
default mindblast = ActiveSkill("Mindblast", 20, 5, "thunder", img="mindblast")
default souldrain = ActiveSkill("Soul Drain", 80, 60, "acid", img="souldrain")
default lavaburst = ActiveSkill("Lava Burst", 20, 5, "fire", img="lavaburst")
default deathmissile = ActiveSkill("Death Missile", 70, 45, "rock", img="deathmissile")
default meteorshower = ActiveSkill("Meteor Shower", 80, 40, "rock", "all", img="meteorshower")
default hellrage = ActiveSkill("Hell Rage", 120, 80, "fire", "all", img="hellrage")
default lifedrain = ActiveSkill("Life Drain", 80, 15, "acid", img="lifedrain")
default devastationbeam = ActiveSkill("Devastation Beam", 30, 5, "fire", "all", img="devastationbeam")
default energybeams = ActiveSkill("Energy Beams", 70, 40, "thunder", "all", img="energybeams")
default giftofangels = ActiveSkill("Gift of Angels", -35, 10, "heal", "ally", 2, img="giftofangels")
# PASSIVE SKILLS (name, sfx=None, img=None, trans=None, lvl=0)
default radar = PassiveSkill("Radar", "heal")
default passive1 = PassiveSkill("Passive Skill 1", "heal")
default passive2 = PassiveSkill("Passive Skill 2", "heal")
