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
        return round(x_array[idx],3)
    
    def inverse_xscale_right(x):
        idx = (np.abs(np.array(y_array_right) - x)).argmin()
        return round(x_array[idx],3)

    def inverse_yscale_top(y):
        idx = (np.abs(np.array(y_array_top) - y)).argmin()
        return round(x_array[idx],3)
    
    def inverse_yscale_bottom(y):
        idx = (np.abs(np.array(y_array_bottom) - y)).argmin()
        return -1*round(x_array[idx],3)

    control_point_fields = []

    with open(topas_path, 'r') as file:
        lines = file.readlines()

    mlc_left_positions = [[] for i in range(80)]
    mlc_right_positions = [[] for i in range(80)]
    energy = ""

    for line in lines:
        if "GantryAngles/Values" in line:
            gantry_angles = line.split("=")[1]
            continue

        elif "CollimatorAngles/Values" in line:
            collimator_angles = line.split("=")[1]
            continue

        elif "CouchAngles/Values" in line:
            couch_angles = line.split("=")[1]
            continue

        elif "SSDs/Values" in line:
            ssd = line.split("=")[1]
            continue

        elif "Depths/Values" in line:
            depths = line.split("=")[1]
            continue

        elif "TransYQVX" in line:
            transyqvx = line.split("=")[1]

        elif "TransXQVY/Values" in line:
            transxqvy = line.split("=")[1]

        elif "Energy/Values" in line:
            energy = line.split("=")[1]

        elif "LeftLeaf" in line and "Pos/Values" in line:
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

    gantry_angles = np.asfarray(list(map(str.strip,gantry_angles.split()[:-1]))).tolist()[1:]
    collimator_angles = np.asfarray(list(map(str.strip,collimator_angles.split()[:-1]))).tolist()[1:]
    couch_angles = np.asfarray(list(map(str.strip,couch_angles.split()[:-1]))).tolist()[1:]
    if energy == "":
        energy = ["6" for i in range(len(couch_angles))]
    else:
        energy = list(map(lambda x: str.replace(x,'"',""),list(map(str.strip,energy.split()))[1:]))
    try: 
        ssd = np.asfarray(list(map(str.strip,ssd.split()[:-1]))).tolist()[1:]
        ssd = [50-float(i) for i in ssd]
    except UnboundLocalError:
        ssd = [90 for i in range(len(gantry_angles))]
    try:
        depths = np.asfarray(list(map(str.strip,depths.split()[:-1]))).tolist()[1:]
        depths = [20-float(i) for i in depths]
    except UnboundLocalError:
        depths = [10 for i in range(len(gantry_angles))]
    top_jaw_positions    = np.asfarray(list(map(str.strip,top_jaw_positions.split()[:-1]))).tolist()[1:]
    bottom_jaw_positions = np.asfarray(list(map(str.strip,bottom_jaw_positions.split()[:-1]))).tolist()[1:]
    try:
        transyqvx = np.asfarray(list(map(str.strip,transyqvx.split()[:-1]))).tolist()[1:]
        transxqvy = np.asfarray(list(map(str.strip,transxqvy.split()[:-1]))).tolist()[1:]
    except UnboundLocalError:
        transyqvx = [0 for i in range(len(gantry_angles))]
        transxqvy = [0 for i in range(len(gantry_angles))]

    if top_jaw_positions[0] < 0:
        top_jaw_positions, bottom_jaw_positions = bottom_jaw_positions, top_jaw_positions

    mlc_left_positions   = np.asfarray(mlc_left_positions).T.tolist()
    mlc_left_positions
    mlc_right_positions  = np.asfarray(mlc_right_positions).T.tolist()
    mlc_right_positions

    for i in range(len(top_jaw_positions)):

        control_point_fields += [[list(zip( list(reversed(list(map(inverse_xscale_left,mlc_left_positions[i])))), list(reversed(list(map(inverse_xscale_right,mlc_right_positions[i])))))), [inverse_yscale_bottom(top_jaw_positions[i]), -1*inverse_yscale_top(bottom_jaw_positions[i]) ]]]
        CF.sequence.append(MLCField(C, CF, control_point_fields[-1][0], control_point_fields[-1][1], gantry_angles[i], collimator_angles[i], couch_angles[i], ssd[i], depths[i], energy[i], i, transyqvx[i], transxqvy[i]))

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

    def right_leaf_overtravel_calc(field_size):
        return -77.12921 - 0.3400335*field_size - 0.00006644729*field_size**2

    def left_leaf_overtravel_calc(field_size):
        return -77.18618 + 0.3438024*field_size - 0.00009227649*field_size**2
    
    if not left:

        if x < 0:
            return round(  right_leaf_overtravel_calc(x)  , 5)
        elif x > 0:
            return round(  -77.5 -((x1 + x2) * 10 + correction(field_size / 0.2))   , 5)
        else:
            return -77.25
    
    else:
        if x < 0:
            return round(  -77.5 -((x1 + x2) * 10 + correction(field_size / 0.2))   , 5)
        elif x > 0:
            return round(  left_leaf_overtravel_calc(x)   , 5)
        else:
            return -77.25


def field_size_calc_jaws(x, top=True):

    def correction(field_size):
        return 10 * (0.00155198 * field_size - 0.0411672)
    
    def top_jaw_overtravel_calc(field_size):
        return -99.95833 - 0.4656239*field_size - 0.00004317857*field_size**2

    def bottom_jaw_overtravel_calc(field_size):
        return -1*top_jaw_overtravel_calc(-1*field_size)


    field_size = abs(x) * 0.2
    cil = 46.2
    r = 8.5  # 13.5 ?
    sad = 98#100
    x1 = field_size * cil / (2 * sad)

    x2 = r * (1 / (np.cos(np.arctan(field_size / (2 * sad)))) - 1)

    if not top:
        if x > 0:
            return round( bottom_jaw_overtravel_calc(x) , 5)
        elif x < 0:
            return round( 99.75+((x1 + x2) * 10 + correction(field_size / 2)) , 5)
        else:
            return 99.75
    else:
        if x < 0:
            return round( top_jaw_overtravel_calc(x) , 5)
        elif x > 0:
            return round( -99.75-((x1 + x2) * 10 + correction(field_size / 2)) , 5)
        else:
            return -99.75