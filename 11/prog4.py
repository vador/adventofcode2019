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


class Logger:
    min_log_level = 0

    def __init__(self):
        self.min_log_level = 0

    def log(self, object_from, log_string, log_level=1):
        if log_level >= self.min_log_level:
            print(log_string)


class Memory:
    PAGESIZE = 1024
    memory_map = None

    def __init__(self):
        self.memory_map = {}

    def _dump(self):
        res_str = " ".join(map(str, self.memory_map[0]))
        return res_str

    def set_instruction(self, program):
        page = self.get_page(0)
        if len(program) > self.PAGESIZE:
            raise NotImplementedError
        for (i, val) in enumerate(program):
            page[i] = val

    def get_page(self, pageid):
        if pageid not in self.memory_map.keys():
            tmp_page = [0] * self.PAGESIZE
            self.memory_map[pageid] = tmp_page
        else:
            tmp_page = self.memory_map[pageid]
        return tmp_page

    def get_pageid_and__offset(self, address):
        return divmod(address, self.PAGESIZE)

    def set_mem(self, address, value):
        (pageid, offset) = self.get_pageid_and__offset(address)
        page = self.get_page(pageid)
        page[offset] = value

    def get_mem(self, address):
        (pageid, offset) = self.get_pageid_and__offset(address)
        page = self.get_page(pageid)
        return page[offset]

    def get_mult_mem(self, address, number=1):
        (pageid, offset) = self.get_pageid_and__offset(address)
        page = self.get_page(pageid)
        if (offset + number) < self.PAGESIZE:
            return page[offset:offset + number]
        else:
            tmp = []
            j = 0
            for i in range(number):
                if offset + j == self.PAGESIZE:
                    pageid += 1
                    offset = 0
                    j = 0
                    page = self.get_page(pageid)
                tmp.append(page[offset + j])
                j += 1
        return tmp


class Program:
    object = "Program"
    memory = None
    ip = 0
    relative_base = 0
    stop = False
    input = None
    output = None
    logger = None

    def parse_paramopcode(self, paramopcode):
        (raw_param, opcode) = divmod(paramopcode, 100)
        (d, c) = divmod(raw_param, 10)
        (d, b) = divmod(d, 10)
        (d, a) = divmod(d, 10)
        return (opcode, a, b, c)

    def output_value(self, val):
        self.output.append(val)

    def get_input_value(self):
        return self.input.pop(0)

    def get_param(self, value, param_mode):
        if param_mode == 0:  # Position mode
            return self.memory.get_mem(value)
        elif param_mode == 1:  # Immediate Mode
            return value
        elif param_mode == 2:  # Relative Mode
            return self.memory.get_mem(self.relative_base + value)
        else:
            raise NotImplementedError

    def get_address_param(self, value, param_mode):
        if param_mode == 0:  # Position mode
            return value
        elif param_mode == 1:
            return value
        elif param_mode == 2:  # Relative Mode
            return self.relative_base + value
        else:
            raise NotImplementedError

    def __str__(self):
        result = "ip: {}[{}]-{}".format(self.ip, self.memory.get_mem(self.ip), self.memory)
        return result

    def __init__(self, instructions):
        self.memory = Memory()
        self.memory.set_instruction(instructions)
        self.ip = 0
        self.relative_base = 0
        self.output = []
        self.input = []
        self.logger = Logger()

    def evaluate_instruction(self):
        if self.memory.get_mem(self.ip) == 99:
            self.stop = True
        else:
            paramopcode = self.memory.get_mem(self.ip)
            (opcode, a, b, c) = self.parse_paramopcode(paramopcode)

            if opcode == 1:
                self.opcode_1_add(a, b, c)
            elif opcode == 2:
                self.opcode_2_mult(a, b, c)
            elif opcode == 3:
                self.opcode_3_stor_input(c)
            elif opcode == 4:
                self.opcode_4_output(c)
            elif opcode == 5:
                self.opcode_5_jtrue(b, c)
            elif opcode == 6:
                self.opcode_6_jfalse(b, c)
            elif opcode == 7:
                self.opcode_7_lt(a, b, c)
            elif opcode == 8:
                self.opcode_8_eq(a, b, c)
            elif opcode == 9:
                self.opcode_9_move_rel_base(c)
            else:
                self.stop = True

    def log_str_3_args(self, oper, reg1, reg2, reg3, a, b, c, val1, val2, val3, new_val):
        log_str = "IP{}\t- {} {}({}) {}({}) {}({}):\t{} {} \t{}->{}".format(self.ip, oper, reg1, c, reg2, b, reg3, a,
                                                                            val1, val2, val3, new_val)
        log_str += "\n" + self.memory._dump()
        return log_str

    def log_str_2_args(self, oper, reg1, reg2, b, c, val1, val2, new_val):
        log_str = "IP{}\t- {} {}({}) {}({}):\t{}\t{}->{}".format(self.ip, oper, reg1, c, reg2, b,
                                                                 val1, val2, new_val)
        log_str += "\n" + self.memory._dump()
        return log_str

    def log_str_1_args(self, oper, reg1, c, val1, new_val):
        log_str = "IP{}\t- {} {}({}) :\t{}->{}".format(self.ip, oper, reg1, c,
                                                       val1, new_val)
        log_str += "\n" + self.memory._dump()
        return log_str

    def opcode_9_move_rel_base(self, c):
        reg1 = self.memory.get_mem(self.ip + 1)
        # val = reg1
        val = self.get_param(reg1, c)
        prev_rel_base = self.relative_base
        self.relative_base += val
        log_str = self.log_str_1_args("MOVR", reg1, c, val, self.relative_base)
        self.logger.log(self.object, log_str)
        self.ip += 2

    def opcode_8_eq(self, a, b, c):
        (reg1, reg2, reg3) = self.memory.get_mult_mem(self.ip + 1, 3)
        val1 = self.get_param(reg1, c)
        val2 = self.get_param(reg2, b)
        if val1 == val2:
            val = 1
        else:
            val = 0
        val3 = self.get_address_param(reg3, a)
        self.memory.set_mem(val3, val)
        log_str = self.log_str_3_args("EQ", reg1, reg2, reg3, a, b, c, val1, val2, val3, val)
        self.logger.log(self.object, log_str)
        self.ip += 4

    def opcode_7_lt(self, a, b, c):
        (reg1, reg2, reg3) = self.memory.get_mult_mem(self.ip + 1, 3)
        val1 = self.get_param(reg1, c)
        val2 = self.get_param(reg2, b)
        val3 = self.get_address_param(reg3, a)
        if val1 < val2:
            val = 1
        else:
            val = 0
        self.memory.set_mem(val3, val)
        log_str = self.log_str_3_args("LT", reg1, reg2, reg3, a, b, c, val1, val2, val3, val)
        self.logger.log(self.object, log_str)
        self.ip += 4

    def opcode_6_jfalse(self, b, c):
        (reg1, reg2) = self.memory.get_mult_mem(self.ip + 1, 2)
        val1 = self.get_param(reg1, c)
        val2 = self.get_param(reg2, b)
        if val1 == 0:
            log_str = self.log_str_2_args("JF", reg1, reg2, b, c, val1, val2, "JMP")
            self.logger.log(self.object, log_str)
            self.ip = val2
        else:
            log_str = self.log_str_2_args("JF", reg1, reg2, b, c, val1, val2, "NOP")
            self.logger.log(self.object, log_str)
            self.ip += 3

    def opcode_5_jtrue(self, b, c):
        (reg1, reg2) = self.memory.get_mult_mem(self.ip + 1, 2)
        val1 = self.get_param(reg1, c)
        val2 = self.get_param(reg2, b)
        if val1 != 0:
            log_str = self.log_str_2_args("JT", reg1, reg2, b, c, val1, val2, "JMP")
            self.logger.log(self.object, log_str)
            self.ip = val2
        else:
            log_str = self.log_str_2_args("JT", reg1, reg2, b, c, val1, val2, "NOP")
            self.logger.log(self.object, log_str)
            self.ip += 3

    def opcode_4_output(self, c):
        reg1 = self.memory.get_mem(self.ip + 1)
        val = self.get_param(reg1, c)
        self.output_value(val)
        log_str = self.log_str_1_args("OUT", reg1, c, "", val)
        self.logger.log(self.object, log_str)

        self.ip += 2

    def opcode_3_stor_input(self, c):
        reg1 = self.memory.get_mem(self.ip + 1)
        val = self.get_input_value()
        reg2 = self.get_address_param(reg1, c)
        self.memory.set_mem(reg2, val)
        log_str = self.log_str_1_args("IN", reg1, c, reg2, val)
        self.logger.log(self.object, log_str)
        self.ip += 2

    def opcode_2_mult(self, a, b, c):
        (reg1, reg2, reg3) = self.memory.get_mult_mem(self.ip + 1, 3)
        val1 = self.get_param(reg1, c)
        val2 = self.get_param(reg2, b)
        val3 = self.get_address_param(reg3, a)
        val = val1 * val2
        self.memory.set_mem(val3, val)
        log_str = self.log_str_3_args("MULT", reg1, reg2, reg3, a, b, c, val1, val2, val3, val)
        self.logger.log(self.object, log_str)
        self.ip += 4

    def opcode_1_add(self, a, b, c):
        (reg1, reg2, reg3) = self.memory.get_mult_mem(self.ip + 1, 3)
        val1 = self.get_param(reg1, c)
        val2 = self.get_param(reg2, b)
        val3 = self.get_address_param(reg3, a)
        val = val1 + val2
        self.memory.set_mem(val3, val)
        log_str = self.log_str_3_args("ADD", reg1, reg2, reg3, a, b, c, val1, val2, val3, val)
        self.logger.log(self.object, log_str)
        self.ip += 4

    def evaluate(self):
        while (not self.stop):
            self.evaluate_instruction()
        return

    def __iter__(self):
        return self

    def __next__(self):
        while (not self.stop):
            self.evaluate_instruction()
            if len(self.output) > 0:
                return self.output.pop(0)
        raise StopIteration


class Robot:
    DIRECTIONS = ["^", ">", "v", "<"]
    OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    direction = None
    position = None
    hull = None

    def __init__(self):
        self.direction = 0
        self.position = (0, 0)
        self.hull = {}

    def move(self, color, rotation):
        self.hull[self.position] = color
        self.direction = (self.direction + (-rotation * 2 + 1)) % 4
        (dx, dy) = self.OFFSETS[self.direction]
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def get_panel_color(self, coord):
        if coord in self.hull:
            return self.hull[coord]
        else:
            return 0

    def get_bounds(self):
        (xmin, xmax, ymin, ymax) = (0, 0, 0, 0)
        for panel in self.hull.keys():
            xmin = min(xmin, panel[0])
            xmax = max(xmax, panel[0])
            ymin = min(ymin, panel[1])
            ymax = max(ymax, panel[1])
        return xmin, xmax, ymin, ymax

    def display_hull(self):
        (xmin, xmax, ymin, ymax) = self.get_bounds()
        display = []
        for row in range(ymax - ymin + 1):
            display.append([" "] * (xmax - xmin + 1))
        for panel in self.hull.keys():
            if self.hull[panel] == 1:
                panel_xmin = panel[0] - xmin
                panel_ymin = panel[1] - ymin
                # print(panel_xmin, panel_ymin)
                display[panel_ymin][xmax - panel_xmin] = "X"
        for (i, row) in enumerate(display):
            display[i] = "".join(row)
        display = "\n".join(display)
        return display


if __name__ == '__main__':

    my_robot = Robot()
    value_loader = LoadValues("input")
    output = value_loader.comma_list_to_intlist()
    int_val = [int(val) for val in output]

    my_prog = Program(int_val)
    my_prog.logger.min_log_level = 2
    my_prog_iter = my_prog.__iter__()
    output = []
    my_prog.input.append(0)
    for val in my_prog_iter:
        output.append(val)
        if len(output) >= 2:
            color = output.pop(0)
            rotation = output.pop(0)
            # print(my_robot.position, my_robot.get_panel_color(my_robot.position), my_robot.direction, (color, rotation))
            my_robot.move(color, rotation)
            my_prog.input.append(my_robot.get_panel_color(my_robot.position))
    print(len(my_robot.hull))

    my_robot = Robot()
    my_prog = Program(int_val)
    my_prog.logger.min_log_level = 2
    my_prog_iter = my_prog.__iter__()
    output = []
    my_prog.input.append(1)
    for val in my_prog_iter:
        output.append(val)
        if len(output) >= 2:
            color = output.pop(0)
            rotation = output.pop(0)
            # print(my_robot.position, my_robot.get_panel_color(my_robot.position), my_robot.direction, (color, rotation))
            my_robot.move(color, rotation)
            my_prog.input.append(my_robot.get_panel_color(my_robot.position))
    print(my_robot.display_hull())
