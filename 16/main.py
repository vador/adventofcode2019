from loadValues import LoadValues
import cProfile, pstats


def build_pattern(i, length):
    base_pattern = [0, 1, 0, -1]
    res = []
    for val in base_pattern:
        res += [val] * i
    fill = res * ((length + 1) // len(res) + 1)
    fill.pop(0)
    return fill[:length]


def build_pattern_list(max):
    pattern_list = []
    for i in range(max):
        pattern_list.append(build_pattern(i + 1, max))
    return pattern_list


def get_units(val):
    (div, res) = divmod(abs(val), 10)
    return res


def multiply_round(digit_list, pattern):
    tmp = [a * b for (a, b) in zip(digit_list, pattern)]
    res = get_units(sum(tmp))
    return res


def round(digit_list, pattern_list):
    res = []
    for (i, val) in enumerate(digit_list):
        res.append(multiply_round(digit_list, pattern_list[i]))
    return res


lv = LoadValues("input")
digit_list = lv.get_digit_list()
print(digit_list)
#digit_list = [1, 2, 3, 4, 5, 6, 7, 8]
digit_list = [int(i) for i in list("80871224585914546619083218645595")]
#digit_list = [int(i) for i in list("69317163492948606335995924319873")]

pr = cProfile.Profile()
pr.enable()
print()
nb_char = len(digit_list)
pattern_list = build_pattern_list(nb_char)
print(len(pattern_list))
res = digit_list
for i in range(100):
    res = round(res, pattern_list)
    print(res)

tmp = [str(i) for i in res[:8]]
print("".join(tmp))
pr.disable()
pr.print_stats()