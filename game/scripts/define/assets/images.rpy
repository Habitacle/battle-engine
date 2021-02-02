image bb1 = "images/bg/1.webp"
image bb2 = "images/bg/2.webp"
image bb3 = "images/bg/3.webp"

image player_battle = TransitionConditionSwitch(Dissolve(0.5, alpha=True),
    "currentplayer == a","images/char/glow/player_battle.webp",
    "a.dead == True","images/char/blank.webp",
    "True", "images/char/player_battle.webp")
image yu_battle = TransitionConditionSwitch(Dissolve(0.5, alpha=True),
    "currentplayer == y","images/char/glow/yu_battle.webp",
    "y.dead == True","images/char/blank.webp",
    "True", "images/char/yu_battle.webp")
image chie_battle = TransitionConditionSwitch(Dissolve(0.5, alpha=True),
    "currentplayer == c","images/char/glow/chie_battle.webp",
    "c.dead == True","images/char/blank.webp",
    "True", "images/char/chie_battle.webp")
image fuuka_battle = TransitionConditionSwitch(Dissolve(0.5, alpha=True),
    "currentplayer == f","images/char/glow/fuuka_battle.webp",
    "f.dead == True","images/char/blank.webp",
    "True", "images/char/fuuka_battle.webp")
image rise_battle = TransitionConditionSwitch(Dissolve(0.5, alpha=True),
    "currentplayer == r","images/char/glow/rise_battle.webp",
    "r.dead == True","images/char/blank.webp",
    "True", "images/char/rise_battle.webp")

image radar_anim = At("images/anim/radar.webp", idle_sway)
