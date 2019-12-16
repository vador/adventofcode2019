import sys
import re
import collections
import math
import heapq
import itertools


class LoadValues:
    file = './input'
    raw_values = None
    processed_values = None

    def __init__(self, data=None, file=True):
        if file:
            if data is not None:
                file_name = data
            else:
                file_name = self.file
            with open(file_name) as f:
                self.raw_values = f.read().splitlines()
        else:
            self.raw_values = list(data)

    def list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = [int(val) for val in raw]
        return self.processed_values

    def comma_list_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = raw[0].split(",")
        return self.processed_values

class AsteroidField:
    field = None
    asteroid_coords = None

    def __init__(self, field):
        self.field = field
        self.parse_field()

    def __str__(self):
        return "\n".join(self.field)

    def get_vector_asteroids(self, ast1, ast2):
        (x1,y1) = ast1
        (x2,y2) = ast2
        return (x2-x1, y2-y1)

    def get_normalized_vector_asteroids(self, ast1, ast2):
        (x,y) = self.get_vector_asteroids(ast1, ast2)
        return self.normalize_vector((x,y))

    def dist(self,ast1, ast2):
        (dx, dy) = self.get_vector_asteroids(ast1, ast2)
        return (math.sqrt(dx*dx+dy*dy))

    def normalize_vector(self, ast):
        (x,y) = ast
        if (x==0) and (y==0):
            return (0,0)
        if x==0:
            return (0, y // abs(y))
        if y==0:
            return (x // abs(x),0)
        z = math.gcd(x,y)
        return (x//z, y//z)

    def parse_field(self):
        coord_list = []
        for j,fields in enumerate(self.field):
            for i,cell in enumerate(self.field[j]):
                if cell == "#":
                    coord_list.append((i,j))
        self.asteroid_coords = coord_list

    def get_visible_asteroids(self, ast):
        (x,y) = ast
        ast_list = {}
        for ast_target in self.asteroid_coords:
            if ast != ast_target:
                norm_coords = self.get_normalized_vector_asteroids(ast, ast_target)
                if norm_coords in ast_list.keys():
                    ast_list[norm_coords].append(ast_target)
                else:
                    ast_list[norm_coords] = [ast_target]
        return ast_list

    def theta(self, ast):
        (x,y)= ast
        (d,m) = divmod(math.atan2(x,-y)+2*3.1416,2*3.1416)
        return m

    def cmp_coords(self, ast1, ast2):
        (x1,y1) = ast1
        (x2,y2) = ast2
        if self.normalize_vector(ast1) == self.normalize_vector(ast2):
            return 0
        theta1 = theta(ast1)
        theta2 = theta(ast2)
        return (theta2-theta1)

def destroy_asteroid(ast_list):
    ast_at_pos = ast_list.pop(0)
    popped = ast_at_pos[1].pop(0)
    if len(ast_at_pos[1]) > 0:
        ast_list.append(ast_at_pos)
    return (popped, ast_list)

if __name__ == '__main__':
    value_loader = LoadValues("input")
    myf = AsteroidField(value_loader.raw_values)
    print(myf)
    myf.parse_field()

    tmp = (myf.get_visible_asteroids((5,8)))
    print(len(tmp), tmp)
    maxnb = -1
    best_ast = None
    for ast in myf.asteroid_coords:
        nb = len(myf.get_visible_asteroids(ast).keys())
        if nb > maxnb:
            maxnb = nb
            best_ast = ast

    print(best_ast, maxnb)
    ast_dict = myf.get_visible_asteroids(best_ast)
    ast_list = []
    for ast in ast_dict.keys():
        ast_list.append((ast, ast_dict[ast]))
    print(ast_list)
    ast_list.sort(key=lambda elem: myf.theta(elem[0]))
    for (vec,dst) in ast_list:
        dst.sort(key=lambda ast2: myf.dist(best_ast,ast2))
    print(ast_list)
    for i in range(200):
        print(destroy_asteroid(ast_list)[0])