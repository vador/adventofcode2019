from loadValues import LoadValues
from program import Program
from queue import Queue


class SpaceMap:
    spaceMap = None
    DIRECTIONS_VALUES = {'N': (1,0),
                 'S': (2,2),
                 'W': (3,1),
                 'E': (4,3)}
    DIRECTIONS_MOVES = {'N': (0, -1),
                        'S': (0, 1),
                        'W': (-1, 0),
                        'E': (1, 0)}

    VALUES_DIRECTION = ['N', 'S', 'W', 'E']
    DIRECTIONS_ORDER = ['N', 'W', 'S', 'E']

    def __init__(self):
        self.spaceMap = {}

    def turnRight(self, direction):
        (res, rel) = self.DIRECTIONS_VALUES[direction]
        rel = (rel - 1) % 4
        return self.DIRECTIONS_ORDER[rel]

    def turnLeft(self, direction):
        (res, rel) = self.DIRECTIONS_VALUES[direction]
        rel = (rel + 1) % 4
        return self.DIRECTIONS_ORDER[rel]

    def coming_from(self, direction):
        (res, rel) = self.DIRECTIONS_VALUES[direction]
        rel = (rel + 2) % 4
        return self.DIRECTIONS_ORDER[rel]

    def set_cell(self, position, content):
        self.spaceMap[position] = content

    def get_cell(self, position):
        if position in self.spaceMap:
            return self.spaceMap[position]
        else:
            return " "

    def is_visited_cell(self, position):
        return position in self.spaceMap

    def get_dest_from_pos_dir(self, position, direction):
        (dx, dy) = self.DIRECTIONS_MOVES[direction]
        (x, y) = position
        return x+dx, y+dy


    def get_bounds(self):
        (xmin, xmax, ymin, ymax) = (0, 0, 0, 0)
        for panel in self.spaceMap.keys():
            xmin = min(xmin, panel[0])
            xmax = max(xmax, panel[0])
            ymin = min(ymin, panel[1])
            ymax = max(ymax, panel[1])
        return xmin, xmax, ymin, ymax


    def display_hull(self, bot_pos=None):
        grid_map = self.build_grid_map(bot_pos)
        for (i, row) in enumerate(grid_map):
            grid_map[i] = "".join(row)
        grid_map = "\n".join(grid_map)
        return grid_map

    def build_grid_map(self, bot_pos=None):
        (xmin, xmax, ymin, ymax) = self.get_bounds()
        grid_map = []
        for row in range(ymax - ymin + 1):
            grid_map.append([" "] * (xmax - xmin + 1))
        for panel in self.spaceMap.keys():
            panel_xmin = panel[0] - xmin
            panel_ymin = panel[1] - ymin
            # print(panel_xmin, panel_ymin)
            grid_map[panel_ymin][panel_xmin] = self.spaceMap[panel]
        if bot_pos is not None:
            (bx, by) = bot_pos
            grid_map[by - ymin][bx - xmin] = "D"
        return grid_map


class Explorer:
    spacemap = None
    program = None
    to_visit_queue = None
    oxygen_pos = None

    def __init__(self, spacemap, program):
        self.spacemap = spacemap
        self.program = program.__iter__()

    def get_move_result(self, dir):
        (input_dir, rel) = self.spacemap.DIRECTIONS_VALUES[dir]
        self.program.input.append(input_dir)
        res = self.program.__next__()
        return res

    def explore(self):
        to_visit = [((0, 0), i, False) for i in self.spacemap.VALUES_DIRECTION]
        cur_pos = (0,0)
        while len(to_visit) > 0:
            (pos, direction, prev) = to_visit.pop()
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            #print(self.spacemap.display_hull(pos))
            #print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

            new_pos = self.spacemap.get_dest_from_pos_dir(pos, direction)
            if prev: # Backtrack
                res = self.get_move_result(direction)
                cur_pos = new_pos
            else:
                if not self.spacemap.is_visited_cell(new_pos): # Dest is has not been visited
                    res = self.get_move_result(direction)
                    ## Fill map and add new nodes to visit
                    if res == 0:
                        self.spacemap.set_cell(new_pos, "#")
                    elif res == 1:
                        to_visit.append(((new_pos), self.spacemap.coming_from(direction), True))
                        to_visit.append(((new_pos), self.spacemap.turnRight(direction), False))
                        to_visit.append(((new_pos), self.spacemap.turnLeft(direction), False))
                        to_visit.append(((new_pos), direction, False))
                        self.spacemap.set_cell(new_pos, ".")
                        cur_pos = new_pos
                    elif res == 2:
                        self.spacemap.set_cell(new_pos,"O")
                        self.oxygen_pos = new_pos
                        to_visit.append(((new_pos), self.spacemap.coming_from(direction), True))
                        to_visit.append(((new_pos), self.spacemap.turnRight(direction), False))
                        to_visit.append(((new_pos), self.spacemap.turnLeft(direction), False))
                        to_visit.append(((new_pos),direction, False))
                        cur_pos = new_pos
        self.spacemap.set_cell((0,0), "X")


    def bfs(self, orig):
        distances = {orig: 0}
        grid_map = self.spacemap.build_grid_map()
        cur_dist = 0
        to_explore = Queue()
        to_explore.put((orig, 0))
        while not to_explore.empty():
            (pos, dist) = to_explore.get()
            dist += 1
            for direction in self.spacemap.DIRECTIONS_ORDER:
                next_pos = self.spacemap.get_dest_from_pos_dir(pos, direction)
                if self.spacemap.spaceMap[next_pos] != "#":
                    if next_pos not in distances.keys():
                        to_explore.put((next_pos, dist))
                        distances[next_pos] = dist
        print(distances)
        return distances