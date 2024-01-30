from .mlc_field import MLCField
import numpy as np

def load_fields_from_topas(topas_path, C, CF):          

    x_array = np.arange(-200, 200.01, 0.01)
    y_array_right = [new_field_calc(x, left=False) for x in x_array]
    y_array_left = [new_field_calc(x, left=True) for x in x_array]
    y_array_top = [field_size_calc_jaws(x, top=True) for x in x_array]
    y_array_bottom = [field_size_calc_jaws(x, top=False) for x in x_array]

    def inverse_xscale_left(x):
        idx = (np.abs(np.array(y_array_left) - x)).argmin()
        return -1*round(x_array[idx],3)
    
    def inverse_xscale_right(x):
        idx = (np.abs(np.array(y_array_right) - x)).argmin()
        return -1*round(x_array[idx],3)

    def inverse_yscale_top(y):
        idx = (np.abs(np.array(y_array_top) - y)).argmin()
        return round(x_array[idx],3)
    
    def inverse_yscale_bottom(y):
        idx = (np.abs(np.array(y_array_bottom) - y)).argmin()
        return round(x_array[idx],3)

    control_point_fields = []

    with open(topas_path, 'r') as file:
        lines = file.readlines()

    top_jaw_positions = []
    bottom_jaw_positions = []
    mlc_left_positions = [[] for i in range(80)]
    mlc_right_positions = [[] for i in range(80)]

    for line in lines:
        if "LeftLeaf" in line and "Pos/Values" in line:
            mlc_left_positions[int(line.split("LeftLeaf")[1].split("Pos")[0])] = list(np.asfarray(list(map(str.strip,line.split("=")[1].split()[:-1])))[1:])
            continue

        elif "RightLeaf" in line and "Pos/Values" in line:
            mlc_right_positions[int(line.split("RightLeaf")[1].split("Pos")[0])] = list(np.asfarray(list(map(str.strip,line.split("=")[1].split()[:-1])))[1:])
            continue

        elif "TopJawPos/Values" in line:
            top_jaw_positions = line.split("=")[1]
            continue

        elif "BottomJawPos/Values" in line:
            bottom_jaw_positions = line.split("=")[1]
            continue

    top_jaw_positions    = np.asfarray(list(map(str.strip,top_jaw_positions.split()[:-1]))).tolist()[1:]
    bottom_jaw_positions = np.asfarray(list(map(str.strip,bottom_jaw_positions.split()[:-1]))).tolist()[1:]
    mlc_left_positions   = np.asfarray(mlc_left_positions).T.tolist()
    mlc_right_positions  = np.asfarray(mlc_right_positions).T.tolist()

    for i in range(len(top_jaw_positions)):

        control_point_fields += [[list(zip( list(map(inverse_xscale_right,mlc_right_positions[i])), list(map(inverse_xscale_left,mlc_left_positions[i])))), [inverse_yscale_top(top_jaw_positions[i]), -1*inverse_yscale_bottom(bottom_jaw_positions[i])]]]
        CF.sequence.append(MLCField(C, CF, control_point_fields[-1][0], control_point_fields[-1][1], 0,0,0, i))

    return

def new_field_calc(x, left=True):

    field_size = abs(x) * 0.2
    def correction(field_size):
        return (
            (-3.88962 * 10 ** -6) * field_size ** 2
            + 0.00190817 * field_size
            - 0.256785
            - 0.06856  # +0.0825 -0.2 mm per side
        )
    cil = 34.28  # +1.3 cm?
    r = 17
    sad = 100
    x1 = field_size * cil / (2 * sad)
    x2 = r * (1 / (np.cos(np.arctan(field_size / (2 * sad)))) - 1)

    if not left:

        if x < 0:
            return round(  -77.5 +((x1 + x2) * 10 + correction(field_size / 0.2))   , 5)
        elif x > 0:
            return round(  -77.5 -((x1 + x2) * 10 + correction(field_size / 0.2))   , 5)
        else:
            return -77.25
    
    else:
        if x < 0:
            return round(  -77.5 -((x1 + x2) * 10 + correction(field_size / 0.2))   , 5)
        elif x > 0:
            return round(  -77.5 +((x1 + x2) * 10 + correction(field_size / 0.2))   , 5)
        else:
            return -77.25


def field_size_calc_jaws(x, top=True):

    def correction(field_size):

        return 10 * (0.00155198 * field_size - 0.0411672)

    field_size = abs(x) * 0.2
    cil = 46.2
    r = 8.5  # 13.5 ?
    sad = 100
    x1 = field_size * cil / (2 * sad)

    x2 = r * (1 / (np.cos(np.arctan(field_size / (2 * sad)))) - 1)

    if not top:
        if x > 0:
            return round( 100+((x1 + x2) * 10 + correction(field_size / 2)) , 5)
        elif x < 0:
            return round( 100-((x1 + x2) * 10 + correction(field_size / 2)) , 5)
        else:
            return 100
    else:
        if x < 0:
            return round( -100+((x1 + x2) * 10 + correction(field_size / 2)) , 5)
        elif x > 0:
            return round( -100-((x1 + x2) * 10 + correction(field_size / 2)) , 5)
        else:
            return -100