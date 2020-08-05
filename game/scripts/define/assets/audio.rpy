define audio.block = "audio/battle/skills/block.ogg"
define audio.fanfare = "audio/game/fanfare.ogg"

label battle_music:
    random:
        play music "audio/battle1.ogg"
        play music "audio/battle2.ogg"
    return

init python:
    def sfx_whoosh():
            randclip = renpy.random.randint(0,5)
            rand_clips = ["audio/battle/whoosh1.ogg", "audio/battle/whoosh2.ogg", "audio/battle/whoosh3.ogg", "audio/battle/whoosh4.ogg", "audio/battle/whoosh5.ogg", "audio/battle/whoosh6.ogg", "audio/battle/whoosh7.ogg"]
            sfx = rand_clips[randclip]
            return sfx
    def sfx_monsterdead():
            randclip = renpy.random.randint(0,2)
            rand_clips = ["audio/battle/monsterdead1.ogg", "audio/battle/monsterdead2.ogg", "audio/battle/monsterdead3.ogg"]
            sfx = rand_clips[randclip]
            return sfx
