VESSEL_SIZE = 10

test_input = [
    "#........................................",
    ".#.......................................",
    "..##.....................................",
    "...###...................................",
    "....###..................................",
    ".....####................................",
    "......#####..............................",
    "......######.............................",
    ".......#######...........................",
    "........########.........................",
    ".........#########.......................",
    "..........#########......................",
    "...........##########....................",
    "...........############..................",
    "............############.................",
    ".............#############...............",
    "..............##############.............",
    "...............###############...........",
    "................###############..........",
    "................#################........",
    ".................########OOOOOOOOOO......",
    "..................#######OOOOOOOOOO#.....",
    "...................######OOOOOOOOOO###...",
    "....................#####OOOOOOOOOO#####.",
    ".....................####OOOOOOOOOO#####.",
    ".....................####OOOOOOOOOO#####.",
    "......................###OOOOOOOOOO#####.",
    ".......................##OOOOOOOOOO#####.",
    "........................#OOOOOOOOOO#####.",
    ".........................OOOOOOOOOO#####.",
    "..........................##############.",
    "..........................##############.",
    "...........................#############.",
    "............................############.",
    ".............................###########."]


def get_value(x, y):
    if (test_input[y][x] == '#') or (test_input[y][x] == 'O'):
        return 1
    else:
        return 0


def is_fitting_vessel(line):
    if line < VESSEL_SIZE-1:
        return False
    (xmin1, xmax1) = coords[line - VESSEL_SIZE + 1]
    (xmin2, xmax2) = coords[line]
    if xmax1 - xmin2 >= VESSEL_SIZE-1:
        return True
    return False


def find_next_line(line):
    # coords are at least as much
    (xminp, xmaxp) = coords[line - 1]
    (xmind, xmaxd) = coords[line - 2]
    res = 0
    delta = xminp - xmind - 1
    while True:
        res = get_value(xminp + delta, line)
        if res == 1:
            break
        delta += 1
    xmin = xminp + delta
    res = 1
    delta = xmaxp - xmaxd - 1
    res = get_value(xmaxp + delta, line)
    if res == 0:
        print("Warning - backtrack")
        delta = 0

    while True:
        res = get_value(xmaxp + delta, line)
        if res == 0:
            break
        delta += 1
    xmax = xmaxp + delta - 1
    return (xmin, xmax)


#
coords = [(0, 0), (1, 1),(2,3)]
cur_line = len(coords)
res = False
while True:
    print("line : ", cur_line, " ", end="")
    (xmin, xmax) = find_next_line(cur_line)
    coords.append((xmin, xmax))
    print((xmin, xmax), " : ", end="")
    res = is_fitting_vessel(cur_line)
    print(res)
    if res == True:
        break
    cur_line += 1

(x_pos, y_pos) = (xmin, cur_line - VESSEL_SIZE +1)
print(x_pos, y_pos)
print(x_pos * 10000 + y_pos)
