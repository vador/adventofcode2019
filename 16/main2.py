from loadValues import LoadValues
import cProfile, pstats
import math

BASE_PATTERN = [0, 1, 0, -1]


def get_units(val):
    (div, res) = divmod(abs(val), 10)
    return res

def get_digit_at(digit_list, pos):
    nb = len(digit_list)
    r_pos = pos % nb
    return digit_list[r_pos]

def get_pattern_at(line, pos):
    # everything zero based
    line_1 = line + 1
    pos_1 = pos + 1
    r_pos = pos_1 % (line_1 * 4)
    v = math.floor(r_pos/line_1)
    return BASE_PATTERN[v]

def calculate(row, digit_list, nb):
    tmp= 0
    for i in range(nb):
        tmp += get_digit_at(digit_list, i) * get_pattern_at(row, i)
    return get_units(tmp)

def get_round(digit_list, nb):
    tmp = []
    for i in range(nb):
        tmp.append(calculate(i, digit_list, nb))
    return tmp

lv = LoadValues("input")
digit_list = lv.get_digit_list()
print(digit_list)
#digit_list = [1, 2, 3, 4, 5, 6, 7, 8]
#digit_list = [int(i) for i in list("80871224585914546619083218645595")]
#digit_list = [int(i) for i in list("69317163492948606335995924319873")]

pr = cProfile.Profile()
pr.enable()
print()
nb_char = len(digit_list)
print("input len :", nb_char)
#print(get_digit_at(digit_list, 0), get_digit_at(digit_list, nb_char))
tmp = digit_list
for i in range(100):
    tmp = get_round(tmp, nb_char)
    print(tmp)
res = [1,2,3,4,5,6,7,8]
tmp = [str(i) for i in res[:8]]
print("".join(tmp))
pr.disable()
pr.print_stats()