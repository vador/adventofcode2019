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
                self.raw_values = list(f)
        else:
            self.raw_values = list(data)
        self.processed_values = self.raw_values

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

    def comma_separated_str_to_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = raw.split(",")
        return self.processed_values

    def list_of_comma_list_to_list_of_intlist(self, raw=None):
        if raw == None:
            raw = self.raw_values
        self.processed_values = [self.comma_separated_str_to_intlist(val) for val in raw]
        return self.processed_values


class GridPoint:
    x = None
    y = None
    directions = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_point_by_direction(self, segment):
        dir = segment[0]
        nb = int(segment[1:])
        (delta_x, delta_y) = self.directions[dir]
        delta_x *= nb
        delta_y *= nb
        destpoint = GridPoint(self.x + delta_x, self.y + delta_y)
        return destpoint

    def move_point_by_vector(self, point):
        destpoint = GridPoint(self.x + point + x, self.y + point.y)
        return destpoint

    def m_dist_to(self, dest):
        return (abs(self.x - dest.x) + abs(self.y - dest.y))

    def __repr__(self):
        return "GridPoint: ({},{})".format(self.x, self.y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


class Segment:
    orig = None
    end = None

    def __init__(self, orig, end):
        self.orig = orig
        self.end = end
        self.normalize()

    def __repr__(self):
        return "Segment : {} {}".format(self.orig, self.end)

    def __eq__(self, other):
        return ((self.orig == other.orig) and (self.end == other.end)) or \
               ((self.orig == other.end) and (self.end == other.orig))

    def vector(self):
        return (self.end.x - self.orig.x), (self.end.y - self.orig.y)

    def normalize(self):
        # segment is either horizontal or vertical
        # if horizontal : left to right
        # if vertival  : bottom to top
        if self.orig.x == self.end.x:
            if self.orig.y > self.end.y:
                (self.orig, self.end) = (self.end, self.orig)
        if self.orig.y == self.end.y:
            if self.orig.x > self.end.x:
                (self.orig, self.end) = (self.end, self.orig)

    def orientation(self):
        if self.orig == self.end:
            return None
        if self.orig.x == self.end.x:
            return "V"
        else:
            return "H"

    def is_val_between(self, x, a, b):
        z = abs(a - x) + abs(b - x) - abs(b - a)
        return (z == 0)

    def intersect_colinear(self, a, b, c, d):
        start = min(a,c)
        end = max(b,d)
        return [x for x in range(start, end)
                if self.is_val_between(x, a, b) and
                self.is_val_between(x, c, d)]

    def intersection(self, other):
        Ax = self.orig.x
        Ay = self.orig.y
        Bx = self.end.x
        By = self.end.y
        Cx = other.orig.x
        Cy = other.orig.y
        Dx = other.end.x
        Dy = other.end.y

        denom = (Bx-Ax)*(Dy-Cy)-(By-Ay)*(Dx-Cx)
        numer = (Ay-Cy)*(Dx-Cx)-(Ax-Cx)*(Dy-Cy)
        numes = (Ay-Cy)*(Bx-Ax)-(Ax-Cx)*(By-Ay)

        if denom == 0:
            # segments are //
            if self.orientation()=="H":
                if self.orig.y != other.orig.y:
                    return []
                else:
                    y = self.orig.y
                    return [(x,y) for x in self.intersect_colinear(self.orig.x, self.end.x, other.orig.x, other.end.x)]
            else:
                if self.orig.x != other.orig.x:
                    return []
                else:
                    x = self.orig.x
                    return [(x,y) for y in self.intersect_colinear(self.orig.y, self.end.y, other.orig.y, other.end.y)]
        else:
            # segments are perpendicular
            seg1 = self
            seg2 = other
            if seg1.orientation() == "V":
                (seg1, seg2) = (seg2, seg1)
            if self.is_val_between(seg2.orig.x, seg1.orig.x, seg1.end.x):
                if self.is_val_between(seg1.orig.y, seg2.orig.y, seg2.end.y):
                    return [(seg2.orig.x, seg1.orig.y)]
                else:
                    return []
            else:
                return []


class WirePath:
    wire_path = []
    cur_point = None
    cur_segment = 0

    def __init__(self, wire_path):
        self.wire_path = wire_path.split(',')
        self.cur_point = GridPoint(0, 0)

    def get_segments(self):
        self.cur_point = GridPoint(0, 0)
        self.cur_segment = 0
        segments = []
        orig = self.cur_point
        dest = self.next_point_in_path()
        while dest is not None:
            segments.append(Segment(orig, dest))
            orig = dest
            dest = self.next_point_in_path()
        return segments


    def next_point_in_path(self):
        orig_point = self.cur_point
        if self.cur_segment >= len(self.wire_path):
            return None
        segment = self.wire_path[self.cur_segment]
        dest_point = orig_point.move_point_by_direction(segment)
        self.cur_point = dest_point
        self.cur_segment += 1
        return dest_point

    def is_val_between(self, x, a, b):
        z = abs(a - x) + abs(b - x) - abs(b - a)
        return (z == 0)

    def is_cell_on_segment(self, point, orig, end):
        if (point.x == orig.x) and (point.x == end.x):
            return self.is_val_between(point.y, orig.y, end.y)
        elif (point.y == orig.y) and (point.y == end.y):
            return self.is_val_between(point.x, orig.x, end.x)
        else:
            return False


    def steps_to_cell(self, point):
        self.cur_point = GridPoint(0, 0)
        self.cur_segment = 0
        is_on_path = False
        steps = 0
        orig = self.cur_point
        dest = self.next_point_in_path()
        while dest is not None:
            if self.is_cell_on_segment(point, orig, dest):
                steps += orig.m_dist_to(point)
                break
            else:
                steps += orig.m_dist_to(dest)
                orig = dest
                dest = self.next_point_in_path()

        return steps

    def is_cell_on_path(self, point):
        self.cur_point = GridPoint(0, 0)
        self.cur_segment = 0
        is_on_path = False
        orig = self.cur_point
        dest = self.next_point_in_path()
        while dest is not None:
            if self.is_cell_on_segment(point, orig, dest):
                is_on_path = True
                break
            else:
                orig = dest
                dest = self.next_point_in_path()
        return is_on_path


if __name__ == '__main__':
    value_loader = LoadValues()
    #proc_values = value_loader.list_of_comma_list_to_list_of_intlist()
    wire1_path = WirePath(value_loader.processed_values[0])
    print(wire1_path)
    wire2_path = WirePath(value_loader.processed_values[1])
    w1_segs = wire1_path.get_segments()
    print(w1_segs)
    w2_segs = wire2_path.get_segments()

    origin = GridPoint(0,0)
    min_dist = 65535
    min_dist_part2 = 65535
    for s1 in w1_segs:
        for s2 in w2_segs:
            cur_intersect = s1.intersection(s2)
            for p in cur_intersect:
                # part1
                cur_dist = abs(p[0]) + abs(p[1])
                if cur_dist < min_dist and cur_dist > 0:
                    min_dist = cur_dist
                    min_p = p
                #part2
                gp = GridPoint(p[0],p[1])
                d1 = wire1_path.steps_to_cell(gp)
                d2 = wire2_path.steps_to_cell(gp)
                if d1+d2 < min_dist_part2 and p != (0,0):
                    min_dist_part2 = d1+d2
                    min_p_part2 = p
    print(min_dist, min_p)
    print(min_dist_part2, min_p_part2)

