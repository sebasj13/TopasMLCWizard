import pydicom as pd
from .mlc_field import MLCField

def load_fields_from_rtplan(rtplan_path, C, CF):
    with pd.dcmread(rtplan_path) as ds:
        control_point_fields = []
        gantry_angles = []
        collimator_angles = []
        couch_angles = []
        ssd = []
        number_of_beams = len(ds.BeamSequence)
        for i in range(number_of_beams):
            mlc_positions = {}
            control_points = len(ds.BeamSequence[i].ControlPointSequence)

            for j in range(control_points):
                try: gantry_angles += [ds.BeamSequence[i].ControlPointSequence[j].GantryAngle]
                except Exception: gantry_angles += [gantry_angles[-1]]
                try: collimator_angles += [ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDeviceAngle]
                except Exception: collimator_angles +=  [collimator_angles[-1]]
                try: couch_angles += [ds.BeamSequence[i].ControlPointSequence[j].PatientSupportAngle]
                except Exception: couch_angles += [couch_angles[-1]]
                try: ssd += [ds.BeamSequence[i].ControlPointSequence[j].SourceToSurfaceDistance]
                except Exception: ssd += [ssd[-1]]
                try:
                    for mlc_index in range(len(ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence)):
                        if ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[mlc_index].RTBeamLimitingDeviceType in ["MLCX","MLCY"] :
                            break
                except Exception: continue

                mlc_positions = []
                for k in range(80):
                    mlc_positions += [[round(ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[mlc_index].LeafJawPositions[k],2),
                                      round(ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[mlc_index].LeafJawPositions[k+80],2),]]
                                       
                for mlc_index in range(len(ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence)):
                    if ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[mlc_index].RTBeamLimitingDeviceType in ["ASYMY"] :
                        break

                jaw_positions = [round(ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[mlc_index].LeafJawPositions[0],2), 
                                 round(ds.BeamSequence[i].ControlPointSequence[j].BeamLimitingDevicePositionSequence[mlc_index].LeafJawPositions[1],2)]
                if j != 0 and jaw_positions[0] == jaw_positions[1]:
                    jaw_positions = control_point_fields[-1][1]

                control_point_fields += [[mlc_positions, jaw_positions]]
        
        ssd = [round(float(x)/10,2) for x in ssd]
        depth = [round(100-ssd[i],2) for i in range(len(ssd))]
        for i in range(len(control_point_fields)):
            CF.sequence.append(MLCField(C, CF, list(reversed(control_point_fields[i][0])), list(reversed(control_point_fields[i][1])), gantry_angles[i], collimator_angles[i], couch_angles[i], ssd[i], depth[i], i))

        return