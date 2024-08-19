import math

def get_tool_position(position_sensor_ros, agent_geometry):
    # Get x, y, orientations from the vehicle
    truck_sensors = {**position_sensor_ros.read()}
    try:
        trailer_joint_angle = truck_sensors['orientations'][1]
    except (IndexError, KeyError):
        trailer_joint_angle = 0
        
    absolut_truck_angle = truck_sensors['orientations'][0]
    absolut_trailer_angle = absolut_truck_angle - trailer_joint_angle

    truck_first_axle_position = agent_geometry['axles'][0]['position']
    truck_rear_position = agent_geometry['rear_joint_position']
  
    # We use the position of the first axle as the global x, y reference for the truck, 
    # and truck-trailer joint point as global x, y reference for the trailer.
    truck_global_reference = truck_first_axle_position
    vector_from_reference_to_rear_position = { 'x': truck_rear_position['x'] - truck_global_reference['x'], 
                                               'y': truck_rear_position['y'] - truck_global_reference['y']}
    
    truck_rear_joint_distance_to_truck_global_reference = math.sqrt(vector_from_reference_to_rear_position['x']**2 +
                                                             vector_from_reference_to_rear_position['y']**2 )
    
    trailer_front_joint_distance_to_trailer_global_reference = 0 # by definition


    trailer = {'pose':{}}
    trailer['pose']['x'] = truck_sensors['x'] - truck_rear_joint_distance_to_truck_global_reference * math.cos(absolut_truck_angle/1000) \
                                              - trailer_front_joint_distance_to_trailer_global_reference * math.cos(absolut_trailer_angle/1000) 
    
    trailer['pose']['y'] = truck_sensors['y'] - truck_rear_joint_distance_to_truck_global_reference * math.sin(absolut_truck_angle/1000) \
                                              - trailer_front_joint_distance_to_trailer_global_reference * math.sin(absolut_trailer_angle/1000) 
    
    trailer['pose']['orientations'] = [absolut_trailer_angle]
    
    trailer['sensors'] =   {  'temperatures':{
                                        'sensor_t1': {
                                            'title':"trailer temperature",
                                            'type' :"number",
                                            'value': 40,
                                            'unit': "oC"}
                        }}

    return trailer
