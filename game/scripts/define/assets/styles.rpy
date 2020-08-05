style pixel:
    font "gui/fonts/alkh.ttf"
    outlines [(3, "#658791", 1, 1)]
    color "#b4c5cb"
    size 40

style dmg_text:
    font "gui/fonts/earwig.ttf"
    color "#000000"
    size 80
    outlines [(4.5, "#ffffff", 3.5, 3.5)]

style battle_playerlvl_text:
    font "gui/fonts/prstart.ttf"
    color "#ffffff"
    outlines [(2, "#00000080", 1, 1)]
    size 16

style battle_playername_text:
    font "gui/fonts/prstart.ttf"
    outlines [(4, "#00000025", 2, 2), (2, "#900c3f", 0, 0)]
    color "#ff5733"
    size 24

style skills_button_text:
    size 40
    anchor (.5,.5)
    align (.5,.5)

init python:
    style.bar_mhp = Style(style.default)
    style.bar_mhp.left_bar = Frame("images/battle/mp_full.png",20,20)
    style.bar_mhp.right_bar = Frame("images/battle/mp_empty.png",20,20)
    style.bar_mhp.xmaximum = 180
    style.bar_mhp.ymaximum = 25

    style.bar_hp = Style(style.default)
    style.bar_hp.left_bar = Frame("images/battle/hp_full.png",20,20)
    style.bar_hp.right_bar = Frame("images/battle/hp_empty.png",20,20)
    style.bar_hp.xmaximum = 213
    style.bar_hp.ymaximum = 40

    style.bar_mp = Style(style.default)
    style.bar_mp.left_bar = Frame("images/battle/mp_full.png",20,20)
    style.bar_mp.right_bar = Frame("images/battle/mp_empty.png",20,20)
    style.bar_mp.xmaximum = 213
    style.bar_mp.ymaximum = 40

style statusgui_text:
    size 35 bold True drop_shadow [(-1,-1),(1,-1),(-1,1),(1,1)]
