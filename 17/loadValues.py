import re


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

    def get_3d_coords(self, raw=None):
        if raw == None:
            raw = self.raw_values
        coords = [tuple(map(int, list(re.findall(r'-?\d+', ln)))) for ln in raw]
        self.processed_values = coords
        return coords

    def parse_element(self, element):
        (quantity, compound) = element.strip().split(" ")
        return compound, int(quantity)

    def get_reactions(self, raw=None):
        reactions = {}
        if raw == None:
            raw = self.raw_values
        for ln in raw:
            parse = ln.split(" =>" )
            components = [self.parse_element(element) for element in parse[0].split(",")]
            (result, qr) = self.parse_element(parse[1])
            reactions[result] = ((result, qr), components)
        return reactions

    def get_digit_list(self, raw = None):
        if raw == None:
            raw = self.raw_values
        tmp = str(raw[0]).strip()
        return [int(i) for i in list(tmp)]

    def strip_lines(self, raw = None):
        if raw == None:
            raw = self.raw_values
        tmp = [line.strip() for line in raw]
        self.processed_values = tmp
        return tmp

if __name__ == '__main__':
    lv = LoadValues("input1")

    print(lv.strip_lines())