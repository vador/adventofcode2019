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

    def find_best_path(self, start_key, keys_obtained, partial_dist=0, shortest_path=sys.maxsize, best_path=[]):
        print("Entering : ", start_key, keys_obtained, partial_dist, len(keys_obtained), len(self.key_pos), shortest_path)
        if len(keys_obtained)+1 == len(self.key_pos):
            print(">>>>End of path :", partial_dist, keys_obtained)
            if partial_dist < shortest_path:
                shortest_path = partial_dist
                best_path = keys_obtained
            return (0, [], shortest_path, best_path)
        (reachable_keys, following_keys) = self.find_reachable_keys(start_key, keys_obtained)
        if partial_dist > shortest_path:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><Pruning :", keys_obtained, partial_dist)
        print("Reachable :", reachable_keys)
        shortest_remaining_path = sys.maxsize
        best_full_path = best_path
        best_remaining_keys = []
        for (next_key, move) in reachable_keys:
            (key_dist, key_path, key_shortest_path, key_full_path) = self.find_best_path(next_key, keys_obtained + [next_key],
                                                                          partial_dist + move,
                                                                          shortest_path)
            if key_dist < shortest_remaining_path:
                shortest_remaining_path = move + key_dist
                best_remaining_keys = [next_key] + key_path
            if key_shortest_path < shortest_path:
                shortest_path = key_shortest_path
                best_full_path = key_full_path
        return (shortest_remaining_path, best_remaining_keys, shortest_path, best_full_path)

    def find_best_path_old(self, start_key, keys_obtained, partial_dist=0, best_found_distance=sys.maxsize):
        print("Entering : ", start_key, keys_obtained, partial_dist, len(keys_obtained), len(self.key_pos))
        if len(keys_obtained)+1 == len(self.key_pos):
            print(">>>>End of path path :", partial_dist, keys_obtained)
            return (0, [])

        (reachable_keys, following_keys) = self.find_reachable_keys(start_key, keys_obtained)
        print("Reachable :", reachable_keys)
        best_path = sys.maxsize #2 *sum([move for (key,move) in following_keys])
        #if (partial_dist+ best_remaining_dist > best_found_distance):
        #    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        #    print("Pruning too long", best_found_distance, partial_dist + best_remaining_dist, keys_obtained)
        #    return (sys.maxsize, [])

        best_keys = []
        for (next_key,move) in reachable_keys:
            #print(" new :")
            #move = reachable_keys[next_key]
            (best_remaining_dist, following_keys) = self.find_best_path_old(next_key,
                                                                            keys_obtained + [next_key],
                                                                            partial_dist + move,
                                                                            best_found_distance)
            #print("Best partial : ", cur_dist+move, " best remain : ", best_remaining_dist)
            if partial_dist + move + best_remaining_dist < best_found_distance:
                best_path = best_remaining_dist
                best_found_distance = partial_dist + move + best_remaining_dist
                print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                best_keys = [next_key] + following_keys
                print("Found ", best_path, best_keys)

        return (best_path, best_keys)

if __name__ == '__main__':
    print()
