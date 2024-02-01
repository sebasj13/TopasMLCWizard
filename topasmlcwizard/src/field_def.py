import os
import numpy as np

header = '\
####################################################################\n\
#                             {}                  #\n\
####################################################################\n\n\
s:Tf/GantryAngles/Function           = "Step"\n\
s:Tf/CollimatorAngles/Function       = "Step"\n\
s:Tf/CouchAngles/Function            = "Step"\n\
dv:Tf/GantryAngles/Times             = {} {} s\n\
dv:Tf/CollimatorAngles/Times         = {} {} s\n\
dv:Tf/CouchAngles/Times              = {} {} s\n\
dv:Tf/GantryAngles/Values            = {} {} deg\n\
dv:Tf/CollimatorAngles/Values        = {} {} deg\n\
dv:Tf/CouchAngles/Values             = {} {} deg\n\n'

materials = '\
#################################################################\n\
#                            MATERIALS                          #\n\
#################################################################\n\n\
includeFile                          = {}Components/IEC_F.txt\n\n\
sv:Ma/LeafMaterial/Components        = 3 "Tungsten" "Nickel" "Iron"\n\
uv:Ma/LeafMaterial/Fractions 	     = 3 0.95 00.0375 0.0125\n\
d:Ma/LeafMaterial/Density            = 18 g/cm3\n\n'

mlcgroup = '\
####################################################################\n\
#                       MULTI LEAF COLLIMATOR                      #\n\
####################################################################\n\n\
s:Ge/MLCGroup/Type                   = "Group"\n\
s:Ge/MLCGroup/Parent        	     = "IEC_F"\n\
d:Ge/MLCGroup/TransZ                 = -399.951 mm + Ge/IEC_F/SSD #311.8+90-1.848...\n\
d:Ge/MLCGroup/RotX                   = 8 mrad\n\n'

placement_left = '\
s:Ge/LeftGroup/Type 	    	     = "Group"\n\
s:Ge/LeftGroup/Parent       	     = "MLCGroup"\n\
d:Ge/LeftGroup/RotX                  = 180 deg\n\n'

placement_right = '\
s:Ge/RightGroup/Type        	     = "Group"\n\
s:Ge/RightGroup/Parent 	    	     = "MLCGroup"\n\
d:Ge/RightGroup/RotY 	    	     = 180 deg\n\n\
#===================COMPONENTS===============#\n\n'

left_leaf_parameters = '\
s:Ge/LeftLeaf{}/Type                 = "TsCAD"\n\
s:Ge/LeftLeaf{}/Parent               = "LeftGroup"\n\
s:Ge/LeftLeaf{}/Material             = "LeafMaterial"\n\
d:Ge/LeftLeaf{}/TransX               = Tf/LeftLeaf{}Pos/Value mm\n\
d:Ge/LeftLeaf{}/TransY               = {} mm\n\
d:Ge/LeftLeaf{}/TransZ               = {} mm\n\
d:Ge/LeftLeaf{}/RotX                 = {} deg\n\
s:Ge/LeftLeaf{}/DrawingStyle         = "Solid"\n\
s:Ge/LeftLeaf{}/InputFile            = "{}CAD/MLC_Leaf"\n\
s:Ge/LeftLeaf{}/FileFormat           = "stl" \n\
d:Ge/LeftLeaf{}/Units                = 1 mm\n\
s:Ge/LeftLeaf{}/Color                = {}\n\
s:Ge/LeftLeaf{}/AssignToRegionNamed  = "ShieldRegion"\n\n\
s:Tf/LeftLeaf{}Pos/Function          = "Step"\n\
dv:Tf/LeftLeaf{}Pos/Times            = {} {} s\n\
dv:Tf/LeftLeaf{}Pos/Values           = {} {} mm\n\n\
'

right_leaf_parameters = '\
s:Ge/RightLeaf{}/Type                = "TsCAD"\n\
s:Ge/RightLeaf{}/Parent              = "RightGroup"\n\
s:Ge/RightLeaf{}/Material            = "LeafMaterial"\n\
d:Ge/RightLeaf{}/TransX              = Tf/RightLeaf{}Pos/Value mm\n\
d:Ge/RightLeaf{}/TransY              = {} mm\n\
d:Ge/RightLeaf{}/TransZ              = {} mm\n\
d:Ge/RightLeaf{}/RotX                = {} deg\n\
s:Ge/RightLeaf{}/DrawingStyle        = "Solid"\n\
s:Ge/RightLeaf{}/InputFile           = "{}CAD/MLC_Leaf"\n\
s:Ge/RightLeaf{}/FileFormat          = "stl"\n\
d:Ge/RightLeaf{}/Units               = 1 mm\n\
s:Ge/RightLeaf{}/Color               = {}\n\
s:Ge/RightLeaf{}/AssignToRegionNamed = "ShieldRegion"\n\n\
s:Tf/RightLeaf{}Pos/Function         = "Step"\n\
dv:Tf/RightLeaf{}Pos/Times           = {} {} s\n\
dv:Tf/RightLeaf{}Pos/Values          = {} {} mm\n\n'

jaws = '\
#################################################################\n\
#                              JAWS                             #\n\
#################################################################\n\n\
s:Ge/BottomJaw/Type                     = "TsCAD"\n\
s:Ge/BottomJaw/Parent                   = "IEC_F"\n\
s:Ge/BottomJaw/Material                 = "LeafMaterial"\n\
d:Ge/BottomJaw/TransX                   = 10 cm\n\
d:Ge/BottomJaw/TransY                   = Tf/BottomJawPos/Value mm\n\
d:Ge/BottomJaw/TransZ                   = -432 mm + Ge/IEC_F/SSD \n\
d:Ge/BottomJaw/RotZ                     = 270 deg\n\
s:Ge/BottomJaw/DrawingStyle             = "Solid"\n\
s:Ge/BottomJaw/InputFile                = "{}CAD/Jaw"\n\
s:Ge/BottomJaw/FileFormat               = "stl" \n\
d:Ge/BottomJaw/Units                    = 1 mm\n\
s:Ge/BottomJaw/Color                    = "Grey160"\n\
s:Ge/BottomJaw/AssignToRegionNamed      = "ShieldRegion"\n\n\
s:Tf/BottomJawPos/Function              = "Step"\n\
dv:Tf/BottomJawPos/Times                = {} {} s\n\
dv:Tf/BottomJawPos/Values               = {} {} mm\n\n\
s:Ge/TopJaw/Type                        = "TsCAD"\n\
s:Ge/TopJaw/Parent                      = "IEC_F"\n\
s:Ge/TopJaw/Material                    = "LeafMaterial"\n\
d:Ge/TopJaw/TransX                      = -10 cm\n\
d:Ge/TopJaw/TransY                      = Tf/TopJawPos/Value mm\n\
d:Ge/TopJaw/TransZ                      = -432 mm + Ge/IEC_F/SSD\n\
d:Ge/TopJaw/RotZ                        = 90 deg\n\
s:Ge/TopJaw/DrawingStyle                = "Solid"\n\
s:Ge/TopJaw/InputFile                   = "{}CAD/Jaw"\n\
s:Ge/TopJaw/FileFormat                  = "stl" \n\
d:Ge/TopJaw/Units                       = 1 mm \n\
s:Ge/TopJaw/Color                       = "Grey160"\n\
s:Ge/TopJaw/AssignToRegionNamed         = "ShieldRegion"\n\n\
s:Tf/TopJawPos/Function                 = "Step"\n\
dv:Tf/TopJawPos/Times                   = {} {} s\n\
dv:Tf/TopJawPos/Values                  = {} {} mm\n\n'


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

    return round((x1 + x2) * 10 + correction(field_size / 0.2), 5)

def right_leaf_overtravel_calc(field_size):

    return -77.12921 - 0.3400335*field_size - 0.00006644729*field_size**2

def left_leaf_overtravel_calc(field_size):
    return -77.18618 + 0.3438024*field_size - 0.00009227649*field_size**2

def leaf_overtravel_calc(field_size):

    return -76.985 - 0.3363666*field_size - 0.00004712396*field_size**2

def field_size_calc_jaws(field_size):
    def correction(field_size):

        return 10 * (0.00155198 * field_size - 0.0411672)

    field_size = field_size * 0.2
    cil = 46.2
    r = 8.5  # 13.5 ?
    sad = 100
    x1 = field_size * cil / (2 * sad)

    x2 = r * (1 / (np.cos(np.arctan(field_size / (2 * sad)))) - 1)

    return round(((x1 + x2) * 10 + correction(field_size / 2)), 5)


def CreateTopasArcSequence(
    planname: str,
    gantry_angles: list,
    collimator_angles: list,
    couch_angles: list,
    left_leaf_positions: list,
    right_leaf_positions: list,
    left_jaw_positions: list,
    right_jaw_positions: list,
    cluster = False,
    materials=materials,
    jaws=jaws,
    mlcgroup=mlcgroup,
    placement_left=placement_left,
    placement_right=placement_right,
):
    if cluster:
        cluster = "../Modell/"
    else:
        cluster = ""
    LeafGap = 90 / 1000
    RotXl = [
        180
        + +np.degrees(np.arctan(0.22 / 90))
        - i * np.degrees(np.arctan(20 / 100)) / 40
        for i in range(1, 41)
    ]
    RotXl.reverse()
    RotX = [
        180
        + -np.degrees(np.arctan(0.22 / 90))
        + i * np.degrees(np.arctan(20 / 100)) / 40
        for i in range(1, 41)
    ]
    for i in RotX:
        RotXl.append(i)

    RotX = RotXl
    RotXR = RotX
    RotXR.reverse()
    TransY = []
    TransZ = []

    for i in range(79):

        theta1 = np.radians(RotXR[i])
        theta2 = np.radians(RotXR[i + 1])
        r1 = np.array(
            ((np.cos(theta1), -np.sin(theta1)), (np.sin(theta1), np.cos(theta1)))
        )
        r2 = np.array(
            ((np.cos(theta2), -np.sin(theta2)), (np.sin(theta2), np.cos(theta2)))
        )
        vector11 = r1.dot(np.array([0.735, 90]))
        vector12 = r1.dot(np.array([-0.735, 90]))
        vector21 = r2.dot(np.array([0.735, 90]))
        vector22 = r2.dot(np.array([-0.735, 90]))
        gamma = np.arctan(0.22 / 90)
        if RotX[i] < 180:
            gamma *= -1

        TransY += [
            LeafGap
            + (vector12[0] - vector22[0])
            - 1.47 * np.cos(theta2)
            - (vector21[1] - vector22[1]) * np.tan(theta2 + gamma)
        ]
        TransZ += [vector12[1] - vector22[1]]  # Offset correction

    TransY.reverse()

    TransY1, TransZ1 = (
        [0],
        [0],
    )
    a, b = np.cumsum(TransY).tolist(), np.cumsum(TransZ).tolist()
    for i in range(len(a)):
        TransY1.append(a[i])
        TransZ1.append(b[i])

    TransZ = TransZ1
    TransY = [i - max(a) / 2 for i in TransY1]
    TransYR = TransY
    TransYR.reverse()

    leftcolors = ['"Grey080"', '"Grey160"'] * 40
    rightcolors = ['"Grey080"', '"Grey160"'] * 40
    leaf_num = 80

    times = " ".join([f"{i+1} " for i in range(len(left_jaw_positions))])[:-1]

    left_jaw_values = []
    right_jaw_values = []

    for j in range(len(left_jaw_positions)):
        if left_jaw_positions[j] < 0:
            left_jaw_values.append(
                -(100 + field_size_calc_jaws(abs(left_jaw_positions[j])))
            )
        elif left_jaw_positions[j] == 0:
            left_jaw_values.append(-100)
        else:
            left_jaw_values.append(
                -(100 - field_size_calc_jaws(abs(left_jaw_positions[j])))
            )

        if right_jaw_positions[j] < 0:
            right_jaw_values.append(
                -(100 - field_size_calc_jaws(abs(right_jaw_positions[j])))
            )
        elif right_jaw_positions[j] == 0:
            right_jaw_values.append(-100)
        else:
            right_jaw_values.append(
                -(100 + field_size_calc_jaws(abs(right_jaw_positions[j])))
            )

    leftjawvalues = " ".join([f"{i} " for i in left_jaw_values])[:-1]
    rightjawvalues = " ".join([f"{-i} " for i in right_jaw_values])[:-1]
    gantry_angle_values = " ".join([f"{i} " for i in gantry_angles])
    collimator_angle_values = " ".join([f"{i} " for i in collimator_angles])
    couch_angle_values = " ".join([f"{i} " for i in couch_angles])

    with open(
        os.path.join(planname + ".txt"),"w") as file:
        file.writelines(
            header.format(
                planname.split("/")[-1],
                len(left_jaw_positions),
                times,
                len(left_jaw_positions),
                times,
                len(left_jaw_positions),
                times,
                len(left_jaw_positions),
                gantry_angle_values,
                len(left_jaw_positions),
                collimator_angle_values,
                len(left_jaw_positions),
                couch_angle_values,              
            )
        )

        file.writelines(materials.format(cluster))
        file.writelines(
            jaws.format(
                cluster,
                len(left_jaw_positions),
                times,
                len(left_jaw_positions),
                leftjawvalues,
                cluster,
                len(left_jaw_positions),
                times,
                len(left_jaw_positions),
                rightjawvalues,
            )
        )
        file.writelines(mlcgroup)
        file.writelines(placement_left)
        file.writelines(placement_right)

        left_leaf_values = []
        right_leaf_values = []
        for i in range(len(left_leaf_positions)):
            temp1 = []
            temp2 = []
            for j in range(len(left_leaf_positions[0])):
                if left_leaf_positions[i][j] < 0:
                    temp1.append(
                        -(77.5 + new_field_calc(abs(left_leaf_positions[i][j])))
                    )
                elif left_leaf_positions[i][j] == 0:
                    temp1.append(-77.25)
                else:
                    temp1.append(
                        left_leaf_overtravel_calc(left_leaf_positions[i][j])
                    )

                if right_leaf_positions[i][j] < 0:
                    temp2.append(
                        right_leaf_overtravel_calc(right_leaf_positions[i][j])
                    )
                elif right_leaf_positions[i][j] == 0:
                    temp2.append(-77.25)
                else:
                    temp2.append(
                        -(77.5 + new_field_calc(abs(right_leaf_positions[i][j])))
                    )
            left_leaf_values.append(temp1)
            right_leaf_values.append(temp2)

        for i in range(leaf_num):

            file.writelines(
                left_leaf_parameters.format(
                    i,
                    i,
                    i,
                    i,
                    i,
                    i,
                    TransY[i],
                    i,
                    TransZ[i],
                    i,
                    RotX[i],
                    i,
                    i,
                    cluster,
                    i,
                    i,
                    i,
                    leftcolors[i],
                    i,
                    i,
                    i,
                    len(left_jaw_positions),
                    times,
                    i,
                    len(left_jaw_positions),
                    " ".join([f"{j[i]} " for j in left_leaf_values])[:-1],
                )
            )
            file.writelines(
                right_leaf_parameters.format(
                    i,
                    i,
                    i,
                    i,
                    i,
                    i,
                    TransYR[leaf_num - 1 - i],
                    i,
                    TransZ[leaf_num - 1 - i],
                    i,
                    RotXR[leaf_num - 1 - i],
                    i,
                    i,
                    cluster,
                    i,
                    i,
                    i,
                    rightcolors[i],
                    i,
                    i,
                    i,
                    len(left_jaw_positions),
                    times,
                    i,
                    len(left_jaw_positions),
                    " ".join([f"{j[i]} " for j in right_leaf_values])[:-1],
                )
            )
    return