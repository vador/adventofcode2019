from queue import Queue


class Graph:
    graph = None
    entrance = None
    exit = None
    maze = None
    portals = None
    boundaries_ext = None
    boundaries_int = None
    portals_by_label = None

    def __init__(self):
        pass

    def build_maze(self, maze):
        self.maze = maze.copy()
        self.string_to_maze(maze)

    def get_boundaries(self):
        maze = self.maze
        up_left = None
        down_right = None
        for j in range(0, len(maze)):
            for i in range(0, len(maze[j])):
                val = self.maze[j][i]
                if val == '.' or val == '#':
                    if up_left is None:
                        up_left = (i, j)
                    down_right = (i, j)
        # upper left and lower right corners for maze
        self.boundaries_ext = (up_left, down_right)
        # find first "inner space or letter"
        (xmin, ymin) = up_left
        (xmax, ymax) = down_right
        up_left = None
        down_right = None
        for j in range(ymin, ymax + 1):
            for i in range(xmin, xmax + 1):
                val = self.maze[j][i]
                if val == ' ' or 'A' <= val <= 'Z':
                    if up_left is None:
                        up_left = (i, j)
                    down_right = (i, j)
        self.boundaries_int = (up_left, down_right)

    def find_portals(self):
        portal_list = []
        # external facing borders
        ((xmin, ymin), (xmax, ymax)) = self.boundaries_ext
        # Outer border
        for i in range(xmin, xmax):
            if self.maze[ymin][i] == '.':
                label = self.maze[ymin - 2][i] + self.maze[ymin - 1][i]
                portal_list.append((label, (i, ymin), 1))
            if self.maze[ymax][i] == '.':
                label = self.maze[ymax + 1][i] + self.maze[ymax + 2][i]
                portal_list.append((label, (i, ymax), 1))
        for j in range(ymin, ymax):
            if self.maze[j][xmin] == '.':
                label = self.maze[j][xmin - 2] + self.maze[j][xmin - 1]
                portal_list.append((label, (xmin, j), 1))
            if self.maze[j][xmax] == '.':
                label = self.maze[j][xmax + 1] + self.maze[j][xmax + 2]
                portal_list.append((label, (xmax, j), 1))

        ((xmin, ymin), (xmax, ymax)) = self.boundaries_int
        for i in range(xmin, xmax):
            if self.maze[ymin - 1][i] == '.':
                label = self.maze[ymin][i] + self.maze[ymin + 1][i]
                portal_list.append((label, (i, ymin - 1), -1))
            if self.maze[ymax + 1][i] == '.':
                label = self.maze[ymax - 1][i] + self.maze[ymax][i]
                portal_list.append((label, (i, ymax+1), -1))
        for j in range(ymin, ymax):
            if self.maze[j][xmin - 1] == '.':
                label = self.maze[j][xmin] + self.maze[j][xmin + 1]
                portal_list.append((label, (xmin-1, j), -1))
            if self.maze[j][xmax + 1] == '.':
                label = self.maze[j][xmax - 1] + self.maze[j][xmax]
                portal_list.append((label, (xmax+1, j), -1))
        portals_by_label = {}
        portals_by_pos = {}
        for (label, pos, z) in portal_list:
            if label in portals_by_label:
                portals_by_label[label].append((pos, z))
            else:
                portals_by_label[label] = [(pos, z)]
            portals_by_pos[pos] = label
        self.portals_by_label = portals_by_label

    def get_direct_neighbours(self, pos):
        neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighb_list = []
        (x, y) = pos
        ((xmin, ymin), (xmax, ymax)) = self.boundaries_ext
        ((xmin_i, ymin_i), (xmax_i, ymax_i)) = self.boundaries_int

        for (dx, dy) in neighbours:
            if (xmin <= (x + dx) <= xmax) and (ymin <= (y + dy) <= ymax):
                if not (xmin_i <= (x + dx) <= xmax_i and ymin_i <= y <= ymax_i):
                    neighb_list.append((x + dx, y + dy))
        return neighb_list

    def build_adjacency_map(self):
        ((xmin, ymin), (xmax, ymax)) = self.boundaries_ext
        ((xmin_i, ymin_i), (xmax_i, ymax_i)) = self.boundaries_int
        graph = {}
        for y in range(ymin, ymax+1):
            for x in range(xmin, xmax+1):
                if self.maze[y][x] == '.':
                    graph[(x, y)] = []
                    neighbours = self.get_direct_neighbours((x, y))
                    for (nbx, nby) in neighbours:
                        if self.maze[nby][nbx] == '.':
                            graph[(x, y)].append(((nbx, nby), 0))
        for label in self.portals_by_label:
            vals = self.portals_by_label[label]
            if len(vals) == 2:
                (pos1, z1) = vals[0]
                (pos2, z2) = vals[1]
                graph[pos1].append(vals[1])
                graph[pos2].append(vals[0])
        self.graph = graph

    def string_to_maze(self, maze):
        self.get_boundaries()
        self.find_portals()
        print(self.portals_by_label)
        self.build_adjacency_map()
        self.entrance = self.portals_by_label["AA"][0][0]
        self.exit = self.portals_by_label["ZZ"][0][0]

    def bfs(self):
        queue = Queue()
        pos = self.entrance
        ex_pos = self.exit
        distances = {}
        queue.put((pos, 0, 0))
        while not queue.empty():
            (cur_cell, z, cur_dist) = queue.get()
            cur_dist += 1
            for (nb, z) in self.graph[cur_cell]:
                if nb not in distances:
                    distances[nb] = cur_dist
                    queue.put((nb, z, cur_dist))
        return distances[self.exit]

    def bfs_alt(self):
        queue = Queue()
        pos = self.entrance
        ex_pos = self.exit
        distances = {}
        queue.put((pos, 0, 0))
        while not queue.empty():
            (cur_cell, z, cur_dist) = queue.get()
            print("Blah : ", cur_cell, z, cur_dist)

            if cur_cell == ex_pos and z == 0:
                return distances[(ex_pos, 0)]
            cur_dist += 1
            for (nb, dz) in self.graph[cur_cell]:
                nz = z+dz
                if nz >= 0:
                    if (nb, nz) not in distances:
                        distances[(nb, nz)] = cur_dist
                        queue.put((nb, nz, cur_dist))
        return distances[(ex_pos, 0)]

if __name__ == '__main__':
    pass
