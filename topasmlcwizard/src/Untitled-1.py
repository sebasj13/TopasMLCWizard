import numpy as np

def right_leaf_overtravel_calc(field_size):

    return -77.12921 - 0.3400335*field_size - 0.00006644729*field_size**2

def left_leaf_overtravel_calc(field_size):
    return -77.18618 + 0.3438024*field_size - 0.00009227649*field_size**2


a = [-200, -180, -160, -140, -120, -100, -80, -60, -40, -20, 0]
b = [right_leaf_overtravel_calc(x) for x in a]

print(b)

def new_field_calc(field_size):
    #For no overtravel
    def correction(field_size):
        return (
            (-3.88962 * 10 ** -6) * field_size ** 2
            + 0.00190817 * field_size
            - 0.256785
            - 0.06856  # +0.0825 -0.2 mm per side
        )

    field_size = field_size * 0.2
    cil = 34.28  # +1.3 cm?
    r = 17
    sad = 100
    x1 = field_size * cil / (2 * sad)

    x2 = r * (1 / (np.cos(np.arctan(field_size / (2 * sad)))) - 1)

    return -(77.5+round((x1 + x2) * 10 + correction(field_size / 0.2), 5))

c = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
d = [new_field_calc(x) for x in c]

print(d)