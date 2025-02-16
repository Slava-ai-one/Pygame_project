def update(naprav):
    if naprav == 0:
        if labyrinth.update_map_right_left(0):
            #scelet.move((-1, 0))
            scelet_enter.x -= 1
            scelet_exit.x -= 1
            main_charecter.x -= 1
            #main_charecter.move((-1, 0))

    elif naprav == 1:
        if labyrinth.update_map_right_left(1):
            #scelet.move((1, 0))
            scelet_enter.x += 1
            scelet_exit.x += 1
            main_charecter.x += 1
            #main_charecter.move((1, 0))
    elif naprav == 2:
        if labyrinth.update_map_top_bottom(1):
            #scelet.move((0, 1))
            scelet_enter.y += 1
            scelet_exit.y += 1
            main_charecter.y += 1
            #main_charecter.move((0, 1))
    elif naprav == 3:
        if labyrinth.update_map_top_bottom(0):
            #scelet.move((0, -1))
            scelet_enter.y -= 1
            scelet_exit.y -= 1
            main_charecter.y -= 1
            #main_charecter.move((0, -1))