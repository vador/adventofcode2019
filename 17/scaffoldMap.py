
class ScaffoldMap:
    scaffoldMap = None

    def __init__(self):
        pass

    def is_intersect(self, pos):
        (x, y) = pos
        nbcol = len(self.scaffoldMap[0])
        nblin = len(self.scaffoldMap)
        if (x == 0) or (y == 0) or (x == nbcol-1) or (y == nblin-1):
            return False
        elif self.scaffoldMap[y][x] != "#":
            return False
        else:
            up = self.scaffoldMap[y-1][x]
            down = self.scaffoldMap[y+1][x]
            left = self.scaffoldMap[y][x-1]
            right = self.scaffoldMap[y][x+1]
            return up == "#" and down == "#" and left == "#" and right == "#"

    def get_intersections(self):
        nbcol = len(self.scaffoldMap[0])
        nblin = len(self.scaffoldMap)
        tmp = []
        for j in range(nblin):
            for i in range(nbcol):
                if self.is_intersect((i,j)):
                    tmp.append((i,j))
        return tmp