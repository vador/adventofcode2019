from loadValues import LoadValues
import cProfile, pstats

def calc_second_half(half_list):
    nb = len(half_list)
    tmp = [0] * nb
    tmp[-1] = half_list[nb-1]
    for i in range(nb//2):
        tmp[nb-i-2] = (tmp[nb-i-1] + half_list[nb-i-2]) % 10
    return tmp

lv = LoadValues("input")
digit_list = lv.get_digit_list()
print(digit_list)
#digit_list = [1, 2, 3, 4, 5, 6, 7, 8]
#digit_list = [int(i) for i in list("80871224585914546619083218645595")]
#digit_list = [int(i) for i in list("69317163492948606335995924319873")]
#digit_list = [int(i) for i in list("03036732577212944063491565474664")]


pr = cProfile.Profile()
pr.enable()
print()
nb_char = len(digit_list)
offset = int("".join([str(i) for i in digit_list[:7]]))
print("Offset : ", offset)

res = digit_list*10000
for i in range(100):
    res = calc_second_half(res)
    #print(res)
    print("Round :", i)

tmp = [str(i) for i in res[offset:offset+8]]
print("".join(tmp))
pr.disable()
pr.print_stats()