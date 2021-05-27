default cookbook = list()
default inv = Inventory("Inventory")

label load_items:
    $ cookbook = list()
    $ player_inv = Inventory("[a.name]")
    # var = Item(name, desc, icon=False, value=0, act=Show("inventory_popup", message="Nothing happened!"), type="item", recipe=False, tags={})
    $ hpotion = Item("Health Potion", "Cures 50 hp", "hpotion", 20, type="cons", tags={'pwr': -30,'sfx': "potion"})
    $ mpotion = Item("Magic Potion", "Restores 50 mp", "mpotion", 20, type="cons", tags={'mp': -50,'sfx': "potion"})
    $ rpotion = Item("Revive Potion", "Revives an out of combat ally", "revive", 300, type="cons", tags={'pwr': -200,'sfx': "potion",'targ': "ko"})
    $ player_inv.take(hpotion,4)
    $ player_inv.take(mpotion,4)
    $ player_inv.take(rpotion,2)
    # $ a.addEquip("hand", "Bow")
    return

init python:
    def getTarget(i):
        if 'targ' in i.tags:
            return i.tags['targ']
        else:
            return "self"

    def itemUsable(i):
        if getTarget(i) == "ko":
            deadplayers = 0
            for p in battle_players:
                if p.dead:
                    deadplayers += 1
            if deadplayers > 0:
                return True
            else:
                return False
        else:
            return True

    def useItem(i):
        global damage
        global mpdmg
        global mp_lost
        global atk_sfx
        global currentplayer
        global recover_hp
        global target
        global s_trans
        global msg_skill
        if 'targ' in i.tags:
            target = i.tags['targ']
        else:
            target = "self"
        if 'trans' in i.tags:
            s_trans = i.tags['targ']
        else:
            s_trans = None
        if 'pwr' in i.tags:
            damage = i.tags['pwr']
        if 'mp' in i.tags:
            mpdmg = i.tags['mp']
        atk_sfx = "audio/items/" + i.tags['sfx'] + ".ogg"
        msg_skill = i.name

screen inventory_inbattle(first_inventory):
    key "mouseup_3" action Hide("inv_tooltip"), Jump("player_skill")
    default crafting_screen = False
    tag menu
    modal True
    frame:
        style_group "invstyle"
        hbox:
            pos 10,10
            spacing 50
            vbox:
                label first_inventory.name
                use inventory_battleview(first_inventory)
                use view_nav(first_inventory)
                textbutton "Cancel" action Jump("player_skill")

screen inventory_battleview(inventory):
    side "c r":
        style_group "invstyle"
        area (0, 0, 700, 500)
        vpgrid id ("vp"+inventory.name):
            draggable True
            mousewheel True
            xsize 700 ysize 500
            if inventory.grid_view:
                cols 3 spacing 10
            else:
                cols 1 spacing 25
            for item in inventory.inv:
                $ name = item[0].name
                $ desc = item[0].desc
                $ value = item[0].value
                $ qty = str(item[1])
                if item[0].type=="cons" and itemUsable(item[0]):
                    hbox:
                        $ icon = "images/inv/" + item[0].icon + ".webp"
                        $ hover_icon = im.Sepia(icon)
                        imagebutton:
                            idle LiveComposite((192,192), (0,0), icon, (0,0), Text(qty))
                            hover LiveComposite((192,192), (0,0), hover_icon, (0,0), Text(qty))
                            action SetVariable("dropitem", item[0]), Return(item[0])
                            hovered Show("inv_tooltip",item=item)
                            unhovered Hide("inv_tooltip")
                        if not inventory.grid_view:
                            vbox:
                                text name
                                text "[desc]"

            ## maintains spacing in empty inventories.
            if len(inventory.inv) == 0:
                add Null(height=192,width=192)

        vbar value YScrollValue("vp"+inventory.name)
