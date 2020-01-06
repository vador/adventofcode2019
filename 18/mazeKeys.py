import sys

from loadValues import LoadValues
from queue import Queue
import math

def is_door(val):
    return 'A' <= val <= 'Z'


def is_key(val):
    return 'a' <= val <= 'z'


class Graph:
    graph = None
    key_pos = None
    door_pos = None
    entrance = None
    maze = None

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

    def get_cell(self, pos):
        (x, y) = pos
        return self.maze[y][x]

    def find_reachable_keys(self, pos, key_list):
        to_visit = Queue()
        to_visit.put((pos, 0))
        visited = {}
        reachable_keys = {}
        while not to_visit.empty():
            (cur_cell, cur_dist) = to_visit.get()
            if cur_cell not in visited.keys():
                #print((cur_cell, cur_dist))
                visited[cur_cell] = cur_dist
                (cur_nb, cell_value) = self.graph[cur_cell]
                if is_key(cell_value):
                    reachable_keys[cell_value] = cur_dist
                for (nb, content) in cur_nb:
                    #print("bla :", nb, content, val)
                    if cell_value == '.' or is_key(cell_value) or cell_value.lower() in key_list or cell_value=='@':
                        #print("Add ", nb, cur_dist+1)
                        to_visit.put((nb, cur_dist + 1))
        return reachable_keys

    def find_best_path(self, pos, keys_obtained, partial_dist=0, best_found_distance=sys.maxsize):
        print("Entering : ", pos, keys_obtained)
        if (partial_dist > best_found_distance):
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            print("Pruning too long", best_found_distance, partial_dist, keys_obtained)
            return (sys.maxsize, [])
        reachable_keys = self.find_reachable_keys(pos, keys_obtained)
        print("Reachable :", reachable_keys)
        best_remaining_dist = sys.maxsize
        best_keys = []
        if len(keys_obtained) == len(self.key_pos):
            return (0, [])
        for next_key in reachable_keys.keys():
            print("Test key : ", next_key, end="")
            if next_key in keys_obtained:
                pass
                print(" already obtained")
            else:
                print(" new :")
                move = reachable_keys[next_key]
                (cur_dist, remaining_keys) = self.find_best_path(self.key_pos[next_key],
                                                                 keys_obtained + [next_key],
                                                                 partial_dist + move,
                                                                 best_found_distance)
                print("Best : ", cur_dist+move, " best : ", best_remaining_dist)
                best_found_distance = min(best_found_distance, partial_dist + move + cur_dist)
                if (cur_dist+move) < best_remaining_dist:
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    best_remaining_dist = cur_dist + move
                    best_keys = [next_key] + remaining_keys
                    print("Found ", best_remaining_dist, best_keys)

        return (best_remaining_dist, best_keys)

if __name__ == '__main__':
    print()
