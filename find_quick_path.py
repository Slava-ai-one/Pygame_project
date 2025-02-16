def find_quick_path(map, start, end):
    err_count = 0
    start_path = start
    end_path = end
    sosedy = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    next_path = []
    tales = {}
    curr_path = (start, start, 0)
    while curr_path[0] != end_path:
        if err_count > 1000:
            return None
        for i in range(4):
            if map.get_tale_invent(curr_path[0][0] + sosedy[i][0], curr_path[0][1] + sosedy[i][1]) == 0:
                sosed = (curr_path[0][0] + sosedy[i][0], curr_path[0][1] + sosedy[i][1])
                if sosed in tales or (sosed, curr_path[0], (curr_path[2] + 1)) in next_path:
                    continue
                next_path.append((sosed, curr_path[0], (curr_path[2] + 1)))
                err_count += 1
        tales[curr_path[0]] = (curr_path[0], curr_path[1], curr_path[2])
        curr_path = next_path[0]
        next_path.pop(0)
    back_to_start_way = []
    while curr_path[0] != start_path:
        back_to_start_way.append(curr_path[0])
        curr_path = tales[curr_path[1]]
    # print(back_to_start_way)
    if back_to_start_way:
        return back_to_start_way[-1]
    else:
        return None