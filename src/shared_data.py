


def shared_data( agent_connector, agent_data, initial_status,
                driving_operation_ros,
                position_sensor_ros,
                vehi_state_ros,
                current_assignment_ros):
    
    initial_sensor =  {    'helyos_agent_control':{
                                        'current_task_progress':{
                                            'title':"Progress of drive operation",
                                            'type': "number",
                                             'value':0,
                                             'unit':"",
                                             'maximum': 1},
                        },
                        'temperatures':{
                                        'sensor_t1': {
                                            'title':"cabine",
                                            'type' :"number",
                                            'value': 30,
                                            'unit': "oC"}
                        },                
                        'actuators':{
                                    'sensor_act1': {
                                        'title':"Tail Lift",
                                        'type' :"string",
                                        'value': 'up',
                                        'unit': ""}
                        },
                            
                        "agent": {
                                    "SoC": {
                                        "title": "HV Battery SoC",
                                        "type": "number",
                                        "description": "Battery state of charge of HV System",
                                        "unit": "%",
                                        "minimum": 0,
                                        "maximum": 100,
                                        "value": 100
                                    },
                                    "Voltage": {
                                        "title": "HV Battery Voltage",
                                        "type": "number",
                                        "description": "Battery voltage of HV System",
                                        "unit": "V",
                                        "minimum": 0,
                                        "maximum": 800,
                                        "value": 723
                                    },
                                    "Velocity": {
                                        "title": "Velocity of the vehicle",
                                        "type": "number",
                                        "description": "Speed of the vehicle",
                                        "unit": "km/h",
                                        "minimum": -15,
                                        "maximum": 80,
                                        "value": 0
                                    }
                        }
                        
            }   
    
    position_sensor_ros.publish({ 'x':agent_data['pose']['x'],
                                  'y':agent_data['pose']['y'],
                                  'orientations':agent_data['pose']['orientations'],
                                  'sensors': initial_sensor})
    
    vehi_state_ros.publish({'agent_state': initial_status, 'CONNECTED_TRAILER': None})


