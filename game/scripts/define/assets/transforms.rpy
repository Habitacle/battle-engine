define move_time = .5
define stand_anchor = (.5, .5)
define move_size = 10

transform idle_x(t=move_time, d=move_size, a=stand_anchor):
    ease t xoffset -d
    ease t xoffset d/2
    pause 1
    repeat

transform idle_y(t=move_time, d=move_size, a=stand_anchor):
    ease t yoffset -d
    ease t yoffset 0
    repeat

transform idle_xy(t=move_time, d=move_size, a=stand_anchor):
    parallel:
        linear t/2 xoffset -d
        linear t/2 xoffset d/2
        linear t/2 xoffset d
        linear t/2 xoffset d/2
        repeat
    parallel:
        easein t yoffset -d
        easeout t yoffset 0
        easein t yoffset d
        easeout t yoffset 0
        repeat

transform idle_shake(t=move_time, d=move_size, a=stand_anchor):
    pause renpy.random.randint(3,6)
    function renpy.curry(_shake_function)(dt=t, dist=d/2)
    xoffset 0 yoffset 0
    renpy.random.randint(1,3)
    repeat

transform idle_sway(e=0.5):
    easein e xoffset -20
    pause e
    easein e xoffset 20
    pause e
    repeat

transform slow_sway(e=1.2):
    easein e xoffset -20
    pause e
    easein e xoffset 20
    pause e
    repeat

transform squeeze:
    pause renpy.random.randint(3,6)
    parallel:
        ease 0.3 yzoom 1.2
        ease 0.3 yzoom 1
        pause 0.2
    parallel:
        easein 0.3 yoffset -60
        easeout 0.3 yoffset 0
        ease 0.1 yoffset -3
        ease 0.1 yoffset 0
    parallel:
        ease 0.3 xzoom 0.7
        ease 0.3 xzoom 1
        pause 0.2
    repeat

transform char_sway(e=1):
    ease e xoffset -30
    ease e xoffset 30
    repeat

transform shaking(t=move_time, d=move_size):
    function renpy.curry(_shake_function)(dt=t, dist=d*2)
    xoffset 0 yoffset 0
    repeat

transform shake_fade(t=move_time, d=move_size):
    function renpy.curry(_shake_function)(dt=t, dist=d*2)
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        parallel:
            linear .25 alpha 0.0
        parallel:
            linear .25 zoom 1.5
    xoffset 0 yoffset 0

init python:
    def _shake_function(trans, st, at, dt=.5, dist=64):
        if st <= dt:
            trans.xoffset = int((dt-st)*dist*(.5-renpy.random.random())*2)
            trans.yoffset = int((dt-st)*dist*(.5-renpy.random.random())*2)
            return 1.0/60
        else:
            return None
