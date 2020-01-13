import sys

from queue import Queue


def is_door(val):
    return 'A' <= val <= 'Z'


def is_key(val):
    return 'a' <= val <= 'z'

class key_list:
    _keys = None

    def __init__(self, keylist=[]):
        self._keys = keylist

    def add_key(self, key):
        self._keys.append(key)

    def are_sufficient_to_reach(self, needed_keys):
        if len(needed_keys) == 0:
            return true
        sufficient = True
        for key in needed_keys:
            if key not in self._keys:
                return False
        return True

class Graph:
    graph = None
    key_pos = None
    door_pos = None
    entrance = None
    maze = None
    key_path = None

    def __init__(self):
        self.graph = {}
        self.key_pos = {}
        self.door_pos = {}

    def build_maze(self, maze):
        maxx = len(maze[0])
        maxy = len(maze)
        self.maze = maze.copy()
        neighbour_cells = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for i in range(maxx):
            for j in range(maxy):
                cell_value = maze[j][i]
                if cell_value != "#":
                    if cell_value == "@":
                        self.entrance = (i, j)
                        self.key_pos['@'] = (i,j)
                    elif is_key(cell_value):
                        self.key_pos[cell_value] = (i, j)
                    elif is_door(cell_value):
                        self.door_pos[cell_value] = (i, j)
                    temp_nb = []
                    for (nbx, nby) in neighbour_cells:
                        val = maze[j + nby][i + nbx]
                        if (val != "#"):
                            temp_nb.append(((i + nbx, j + nby), val))
                    self.graph[(i, j)] = (temp_nb, cell_value)
        self.key_path = {}
        for key in self.key_pos:
            self.key_path[key] = self.build_path_from_key(key)

    def get_cell(self, pos):
        (x, y) = pos
        return self.maze[y][x]

    def find_reachable_keys(self, start_key, key_list):
        reachable_keys = []
        remaining_keys = []
        key_path = self.key_path[start_key]
        for key in key_path.keys():
            if key not in key_list:
                (dist, needed_keys) = key_path[key]
                remaining_keys.append((key, dist))
                if self.are_sufficient_to_reach(key_list, needed_keys):
                    reachable_keys.append((key, dist))
        return (reachable_keys, remaining_keys)

    def build_path_from_key(self, start_key):
        to_visit = Queue()
        pos = self.key_pos[start_key]
        needed_keys = []
        to_visit.put((pos, 0, needed_keys))
        visited = {}
        path = {}
        while not to_visit.empty():
            (cur_cell, cur_dist, needed_keys) = to_visit.get()
            if cur_cell not in visited.keys():
                #print((cur_cell, cur_dist))
                visited[cur_cell] = cur_dist
                (cur_nb, cell_value) = self.graph[cur_cell]
                if is_key(cell_value):
                    path[cell_value] = (cur_dist, needed_keys)
                for (nb, content) in cur_nb:
                    #print("bla :", nb, content, val)
                    if content == '.' or content =='@' or is_key(content):
                        #print("Add ", nb, cur_dist+1)
                        to_visit.put((nb, cur_dist + 1, needed_keys))
                    if content >= 'A' and content <= 'Z':
                        to_visit.put((nb, cur_dist + 1, needed_keys+ [content.lower()]))
        return path

    def are_sufficient_to_reach(self, obtained_keys, needed_keys):
        if len(needed_keys) == 0:
            return True
        sufficient = True
        for key in needed_keys:
            if key not in obtained_keys:
                return False
        return True

    def get_neighbours(self, pos):
        (x, y) = pos
        res = []
        neighbour_cells = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for (dx, dy) in neighbour_cells:
            res.append(((x+dx, y+dy), self.maze[y+dy][x+dx]))
        return res

    def is_reachable_cell(self, cell_value, keys_obtained):
        if cell_value == ".":
            return True
        if cell_value == "@":
            return True
        if is_key(cell_value):
            return True
        if is_door(cell_value) and cell_value.lower() in keys_obtained:
            return True
        return False

    def find_best_path_from_entrance(self):
        all_key = frozenset([key for key in self.key_pos.keys()^{'@'}])

        visited = {}
        to_visit = Queue()
        keys_obtained = frozenset()
        to_visit.put((0, self.entrance, keys_obtained))
        while not to_visit.empty():
            (cur_dist, cur_pos, keys_obtained) = to_visit.get()
            cur_dist +=1
            for (neighbour, cell_value) in self.get_neighbours(cur_pos):
                if self.is_reachable_cell(cell_value, keys_obtained):
                    if is_key(cell_value):
                        keys_obtained_new = keys_obtained | {cell_value}
                        if (neighbour, keys_obtained_new) not in visited:
                            visited[(neighbour, keys_obtained_new)] = cur_dist
                            to_visit.put((cur_dist, neighbour, keys_obtained_new))
                    else:
                        if (neighbour, keys_obtained) not in visited:
                            visited[(neighbour, keys_obtained)] = cur_dist
                            to_visit.put((cur_dist, neighbour, keys_obtained))
        best_dist = 65535
        print(visited)
        for candidate in all_key:
            cur_dist = visited[(self.key_pos[candidate], all_key)]
            if cur_dist < best_dist:
                best_dist = cur_dist
        return best_dist



        return start_pos

if __name__ == '__main__':
    print()
