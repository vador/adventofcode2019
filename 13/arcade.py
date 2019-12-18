import re

class Logger:
    min_log_level = 0

    def __init__(self):
        self.min_log_level = 0

    def log(self, object_from, log_string, log_level=1):
        if log_level >= self.min_log_level:
            print(log_string)



class Arcade:
    tiles = None
    logger = None
    ball_coords = None

    def __init__(self):
        self.tiles = {}
        self.logger = Logger()

    def set_tile(self, coords, content):
        self.tiles[coords] = content
        if content == 4:
            self.ball_coords = coords
        self.logger.log("Arcade", "{} - {}".format(coords, content))

    def count_blocks(self):
        cnt = 0
        for tile in self.tiles:
            if self.tiles[tile] == 2:
                cnt += 1
        return cnt
