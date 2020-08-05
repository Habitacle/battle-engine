init python:
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
                c.hp = 1

    def restorehp():
        for c in party_list:
            c.hp = c.hpmax

    def restoremp():
        for c in party_list:
            c.mp = c.mpmax

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
        currentplayer.mp -= mp_lost
        currentplayer.hp -= hp_lost
        player_inv.drop(dropitem)
        renpy.pause(1, hard=True)
        playersChk()
        renpy.hide_screen("monster_dmg")
        renpy.sound.stop()

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
                msg_mons = m.name
                message = "m_dead"
                renpy.pause(1)
                renpy.play(sfx_monsterdead())
                renpy.pause(0.5)
                message = "none"
                monsters_dead += 1
                m.dead = True
                renpy.sound.stop()
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
