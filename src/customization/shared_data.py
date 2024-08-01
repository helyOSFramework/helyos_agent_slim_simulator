# Use this module to customize the sensors initial and to access the communication channels.

from customization.agent_sensors import get_agent_sensors


def shared_data( agent_connector, agent_data, initial_status,
                driving_operation_ros,
                position_sensor_ros,
                vehi_state_ros,
                current_assignment_ros):
    
    initial_sensor =  {  'helyos_agent_control':{
                                        'current_task_progress':{
                                            'title':"Progress of drive operation",
                                            'type': "number",
                                             'value':0,
                                             'unit':"",
                                             'maximum': 1},
                        }, **get_agent_sensors(position_sensor_ros)}
                        
    
    position_sensor_ros.publish({ 'x':agent_data['pose']['x'],
                                  'y':agent_data['pose']['y'],
                                  'orientations':agent_data['pose']['orientations'],
                                  'sensors': initial_sensor})
    
    vehi_state_ros.publish({'agent_state': initial_status, 'CONNECTED_TRAILER': None})
