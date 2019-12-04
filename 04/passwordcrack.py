

class Password:

    def is_valid_password(self, candidate):
        has_repeating = False
        is_ascending = True
        str_candidate = str(candidate)
        cur_char = str_candidate[0]
        for char in str_candidate[1:]:
            if cur_char == char:
                has_repeating = True
            if cur_char > char:
                is_ascending = False
            cur_char = char
        return has_repeating and is_ascending

    def is_password_valid_strict(self, candidate):
        double_repeating = []
        multiple_repeating = []
        has_repeating = False
        is_ascending = True
        str_candidate = str(candidate)
        cur_char = str_candidate[0]
        is_repeating = False
        for char in str_candidate[1:]:
            if cur_char == char:
                if is_repeating:
                    multiple_repeating.append(char)
                else:
                    double_repeating.append(char)
                is_repeating = True
            else:
                is_repeating = False

            if cur_char > char:
                is_ascending = False
            cur_char = char
        for char in double_repeating:
            if char not in multiple_repeating:
                has_repeating = True
        return has_repeating and is_ascending

    def password_variation(self, candidate):
        list_candidate = [int(i) for i in str(candidate)]
        l1 = list_candidate[1:]
        l2 = list_candidate[:-1]
        return map(lambda t: t[0]-t[1],zip(l1,l2))



p = Password()
print(p.is_valid_password(111111))
print(p.is_valid_password(223450))
print(p.is_valid_password(123789))
print(p.is_valid_password(488999))
print("STRICT")
print(p.is_password_valid_strict(488999))
print(p.is_password_valid_strict(123444))
print(p.is_password_valid_strict(111122))


count = 0
count_strict = 0
for candidate in range(145852,616942+1):
    #print(candidate, p.is_valid_password(candidate))

    if p.is_valid_password(candidate):
        count += 1
    if p.is_password_valid_strict(candidate):
        count_strict += 1

print(count)
print(count_strict)
