default name = "Player"
default currentplayer = "[name]"
default eventrunning = False
default _game_menu_screen = "preferences"
init python:
    if not renpy.variant("touch"):
        config.mouse = {"default":[ ("images/cursor.png", 1, 1) ] }

label load_setup:
    if not name:
        $ name = "Player"
    $ a.name = name
    $ magicheal.addSkill(a) # add new skills
    $ defenseup.addSkill(c)
    $ magicswap.addSkill(y)
    call load_monsters
    call load_items
    $ party_list = [a,y,c,f,r] # initial party list, including main character
    $ fixedset = "set 1"
    $ wild_monsters = [mon1,mon2,mon3,mon4,mon5,mon6,mon7,mon8,mon9,mon10,mon11]
    $ restorehp()
    $ restoremp()
    return
