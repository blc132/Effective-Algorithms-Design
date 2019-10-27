def parse_int(s, base=10, val=False):
    if s.isdigit():
        return int(s, base)
    else:
        return val


def ptype(value):
    print(type(value))


def lets_say_its_inf():
    return 9999999


def get_all_ints_from_string(value):
    array = []
    for t in value.split():
        try:
            array.append(int(t))
        except ValueError:
            pass
    return array
