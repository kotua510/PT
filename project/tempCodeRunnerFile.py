for pos in bad_positions:
            bad = Bad((pos[0], pos[1], 40, 40), night, knife_rawrect, bomb_rawrect, map)
            globals.bad_group.add(bad, layer=2)