label start:
    call load_setup
    jump battle_loop

label battle_loop:
    call battle
    $ restorehp()
    $ restoremp()
    jump battle_loop
