#!/bin/python3

def get_pos_of(grid, exp):
    for y in range(len(grid)):
        for x in range(len(grid[0])): # all rows should be the same size
            if grid[y][x] == exp:
                return y, x
    raise ValueError(f"Didnt find expression {exp} in grid.")

def path_finder(startpos, endpos, cmds):
    dx = endpos[1] - startpos[1]
    dy = endpos[0] - startpos[0]

    if dx > 0:
        cmds.append(f"east {dx}")
    elif dx < 0:
        cmds.append(f"west {-dx}")

    if dy > 0:
        cmds.append(f"south {dy}")
    elif dy < 0:
        cmds.append(f"north {-dy}")

    return cmds

def parse_file(filepath):
    with open(filepath) as f:
        rawfile = f.read()

    rawfile = rawfile.split("\n\n") # very smort
    if len(rawfile) != 2:
        print("didnt find the 2 parts.")
        exit(1)
    
    # wi stands for weight info
    wi_raw, grid = rawfile[0], rawfile[1]
    wi_dict = {}
    for wi_raw_row in wi_raw.split("\n"): #this exclued the last row that is empty i think
        wi_raw_row = wi_raw_row.split("=")
        if len(wi_raw_row) != 2:
            print(f"the weight info ({wi_raw_row}) is has too many or to less equal signs.")
            exit(1)
        
        wi_obj_name, wi_obj_weight = wi_raw_row[0], wi_raw_row[1]
        if len(wi_obj_name) != 1: # i dont really need this but its here anyways
            print("all weight info names are one char long. this one isnt for whatever reason...")
            exit(1)

        if wi_obj_weight == "":
            wi_obj_weight = -1

        try:
            wi_obj_weight = int(wi_obj_weight)
        except ValueError:
            print(f"the object {wi_obj_name} has an invalid weight.")
            exit(1)

        wi_dict[wi_obj_name] = wi_obj_weight

    # this checks if there are 2 start positions or some stupid stuff like that
    tmp_grid = grid
    tmp_grid = tmp_grid.replace(".", "")
    tmp_grid = tmp_grid.replace("\n", "")
    existing_exps = []
    for exp in tmp_grid:
        if exp not in existing_exps:
            existing_exps.append(exp)
        else:
            print(f"there are 2 or more {exp} in the garden thats not right is it?")
            exit(1)
    
    if "$" not in existing_exps:
        print("there is no place where the robot can start...")


    grid = [list(line) for line in grid.split("\n")] # my shitty format
    
    # are u tryna fool me???
    row_len = -1
    for row in grid:
        if row_len != -1:
            if len(row) != row_len:
                print("the rows are not the same size")
                exit(1)
        else:
            row_len = len(row)

    return grid, wi_dict 

def is_arr_sorted(arr):
    prev_biggest = 999999999 # big number (:
    for value in arr:
        if value > prev_biggest:
            return False
        prev_biggest = value
    return True


def swap(arr, pos1, pos2, moves):
    if arr[pos1] != -1 and arr[pos2] != -1:
        raise ValueError("both positions are not empty!")

    if arr[pos1] == -1:
        raise ValueError("first position empty!")

    if arr[pos2] != -1:
        raise ValueError("second position not empty!")

    moves.append((pos1, pos2))

    tmp_val = arr[pos1]
    arr[pos1] = arr[pos2]
    arr[pos2] = tmp_val
    return arr


def bubble_sort(arr):
    moves = []

    while not is_arr_sorted(arr):
        for pos, val in enumerate(arr):
            if pos == len(arr) - 1:
                continue

            if (arr[(len(arr) - 1)] != -1) and (val == -1):
                arr = swap(arr, len(arr) - 1, pos, moves)

            elif (not val >= arr[pos+1]) and (arr[len(arr) - 1] == -1):
                if val == -1 and arr[pos + 1] != -1:
                    arr = swap(arr, pos + 1, pos, moves)
                else:
                    arr = swap(arr, pos, len(arr) - 1, moves)
                    arr = swap(arr, pos + 1, pos, moves)
                    arr = swap(arr, len(arr) - 1, pos + 1, moves)

    return moves

def dict_to_arr(wi_dict, wi_order):
    sorted_dict = {key: wi_dict[key] for key in wi_order}
    return list(sorted_dict.values())

def moves_to_point_names(moves, wi_order):
    out_moves = []
    for pos1, pos2 in moves:
        out_moves.append((wi_order[pos1], wi_order[pos2]))
    return out_moves

def germanize_commands(inp):
    out = []
    for cmd in inp:
        if cmd == "drop":
            out.append("gegenstand_absetzen")
        elif cmd == "pickup":
            out.append("gegenstand_aufheben")
        elif "north" in cmd:
            cmd = cmd.replace("north", "fahre_norden")
            out.append(cmd)
        elif "south" in cmd:
            cmd = cmd.replace("south", "fahre_sueden")
            out.append(cmd)
        elif "east" in cmd:
            cmd = cmd.replace("east", "fahre_osten")
            out.append(cmd)
        elif "west" in cmd:
            cmd = cmd.replace("west", "fahre_westen")
            out.append(cmd)
        else:
            raise ValueError("invalid command")
    
    return "\n".join(out)


if __name__=="__main__":
    garden, wi_info = parse_file("garden.txt")
    
    bubble_useable_arr = dict_to_arr(wi_info, sorted("".join(wi_info.keys())))
    moves = bubble_sort(bubble_useable_arr)
    moves = moves_to_point_names(moves, sorted("".join(wi_info.keys())))
    
    commands = []
    robo_start_pos = get_pos_of(garden, "$")
    path_finder(robo_start_pos, get_pos_of(garden, moves[0][0]), commands)
    for i, move in enumerate(moves):
        commands.append("pickup")
        path_finder(get_pos_of(garden, move[0]), get_pos_of(garden, move[1]), commands)
        commands.append("drop")
        if i != len(moves) - 1:
            path_finder(get_pos_of(garden, move[1]), get_pos_of(garden, moves[i +1][0]), commands)

    commands = germanize_commands(commands)
    with open("cmds.txt", "w") as f:
        f.write(commands)
    
    