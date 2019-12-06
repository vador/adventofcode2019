import sys
import re
import collections
import math
import heapq


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

def get_orbit_tuples(values):
    res = []
    for val in values:
        temp = val.split(')')
        (parent, child) = (temp[0], temp[1])
        res.append((parent, child))
    return res

class Orbit:
    parents = None
    dists =  None
    down_from_you = None
    down_from_santa = None

    def __init__(self):
        self.parents = {}
        self.dists = {}

    def build_dict(self,values):
        for val in values:
            parent = val[0]
            child = val[1]
            self.parents[child] = parent
        self.parents["COM"] = "COM"
        self.dists["COM"] = 0

    def get_dist(self, planet):
        if planet in self.dists:
            return self.dists[planet]
        else:
            tmp = self.get_dist(self.parents[planet]) + 1
            self.dists[planet] = tmp
            return tmp

    def get_all_dists(self):
        total = 0
        for planet in self.parents.keys():
            total += self.get_dist(planet)
        return total


    def get_down_from(self, planet):
        res = {}
        cnt = 0
        cur_planet = planet
        while cur_planet != "COM":
            cur_planet = self.parents[cur_planet]
            res[cur_planet] = cnt
            cnt += 1
        return res

    def orbital_transferts(self):
        self.down_from_you = self.get_down_from("YOU")
        self.down_from_santa = self.get_down_from("SAN")
        you_nodes = set(self.down_from_you.keys())
        san_nodes = set(self.down_from_santa.keys())
        common_nodes = you_nodes.intersection(san_nodes)
        min_transfert = 65535
        for node in common_nodes:
            cur_transferts = self.down_from_santa[node] + self.down_from_you[node]
            if cur_transferts < min_transfert:
                min_transfert = cur_transferts
        return min_transfert

if __name__ == '__main__':
    value_loader = LoadValues()
    print(value_loader)
    mo = Orbit()
    processed_values = get_orbit_tuples(value_loader.raw_values)
    mo.build_dict(processed_values)
    print(processed_values)

    #print(mo.get_dist("3ZP"))
    print(mo.get_all_dists())
    print(mo.orbital_transferts())

