init python:
    def monsterTurns():
        global message
        global battleEnd
        global hit_t
        global missed_t
        global skill_t
        global msg_mons
        global atk_sfx
        global use_skill
        for m in battle_monsters:
            hit_t = []
            missed_t = []
            skill_t = []
            use_skill = False
            if not m.dead:
                message = "none"
                if not battleEnd:
                    monsterTarg(m)
                    renpy.play(sfx_whoosh.draw())
                    renpy.pause(0.3, hard=True)
                    renpy.play(atk_sfx)
                    msg_mons = m.name
                    if use_skill:
                        msg_skill = b_skill.name
                        message = "m_skill"
                    else:
                        message = "m_atk"
                    for t in picked_targs:
                        monsterAtk(m, t)

                    m.state = None
                    renpy.show_screen("player_dmg")
                    renpy.pause(0.2, hard=True)
                    renpy.pause(1.0)
                    renpy.hide_screen("player_dmg")
                    playersChk()

    def monsterTarg(m):
        global picked_targs
        global alive_players
        global atk_sfx
        global b_skill
        global use_skill
        global roll_target
        playersCnt()
        targs = 1
        picked_targs = []
        atk_sfx = "audio/battle/monsters/" + m.sfx_atk + ".ogg"
        if m.skills:
            use_skill = renpy.random.choice([True, False])
            if use_skill:
                b_skill = renpy.random.choice(m.skills)
                b_skill.useSkill()
                if b_skill.targ == "all":
                    picked_targs = alive_players
                    return
                else:
                    targs = b_skill.targs
        while targs > 0:
            roll_target = renpy.random.choice(alive_players)
            picked_targs.append(roll_target)
            targs -= 1

    def monsterAtk(m, p):
        global hit_t
        global missed_t
        m.state = "attacking"
        monsterDmg(m, p)
        if accFormula(m, p):
            if skillChk(p):
                hit_t.append(p)
                p._hp -= m_damage
                roll_shake = renpy.random.randint(1,2)
                if roll_shake == 1:
                    renpy.with_statement(hpunch)
                if roll_shake == 2:
                    renpy.with_statement(vpunch)

    def monsterDmg(m, p):
        global roll_target
        global m_damage
        global damage
        global currdmg
        global use_skill
        turnbonus = 0
        if use_skill:
            currdmg = damage
        else:
            currdmg = int(m.atk*1.1 - (m.atk * renpy.random.randint(1,20) / 100))
        if p.defending == True:
            turnbonus += 1*p.lvl
            renpy.play("audio/battle/skills/block.ogg")
        m_damage = currdmg*currdmg/(currdmg+p.dfn+p.bonus_dfn+turnbonus)

    def monsterImg(m):
        if m.state == "attacking":
            return im.MatrixColor(getImage(m), im.matrix.tint(1,.5,.5))
        if m.state == "hit":
            return im.MatrixColor(getImage(m), im.matrix.tint(1,.5,.5))
        if m.state == "heal": # green
            return im.MatrixColor(getImage(m), im.matrix.tint(.5,1,.5))
        if m.state == "dying":
            return im.MatrixColor(getImage(m), im.matrix.invert())
        if m.state == "other": # blue
            return im.MatrixColor(getImage(m), im.matrix.tint(.5,.5,1))
        if m.state == "other2": # hue
            return im.MatrixColor(getImage(m), im.matrix.hue(90))
        else:
            return getImage(m)
