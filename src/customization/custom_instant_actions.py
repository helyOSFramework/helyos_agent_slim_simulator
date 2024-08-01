

import json, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connect_tool import tool_connection

AGENTS_DL_EXCHANGE = os.environ.get('AGENTS_UL_EXCHANGE', 'xchange_helyos.agents.dl')

def my_custom_callback(position_sensor_ros, driving_operation_ros, vehi_state_ros, agentConnector, datareq_rpc, ch, sender, received_str):
    print("not helyos-related instant action", received_str)
    agent_data = position_sensor_ros.read()    
    operation_commands = driving_operation_ros.read()

    try: 
        message = json.loads(received_str)['message']
        print(message)
        command =  json.loads(message) 
    except:
        print("\nAgent does not know how interpret the command:", received_str[0:50])
        return
    
    sensor_patch = {}

    try:
        if "connect_trailer" in command['body'] or  "connect tool" in command['body']:
            return tool_connection(command['body'], vehi_state_ros,position_sensor_ros, agentConnector.helyos_client, datareq_rpc)

        if "pause operation" == command['body']:     
            driving_operation_ros.publish({**operation_commands, 'PAUSE_ASSIGNMENT': True})
            sensor_patch = {  'instant_actions_response':{
                                    'task_control':{
                                            'title':"Task status",
                                            'type': "string",
                                            'value':"paused",
                                            'unit':""},
                                    }
                    }    

        if "resume operation" == command['body']:                                                
            driving_operation_ros.publish({**operation_commands, 'PAUSE_ASSIGNMENT': False})
            sensor_patch = {  'instant_actions_response':{
                                        'task_control':{
                                                'title':"Task status",
                                                'type': "string",
                                                'value':"normal",
                                                'unit':""},
                                        }
                            }   

        if "pause_publish_sensors"  == command['body']: 
            vehi_state_ros.publish({**vehi_state_ros.read(), 'pause_publish_sensors':True })

        if "resume_publish_sensors"  == command['body']: 
            vehi_state_ros.publish({**vehi_state_ros.read(), 'pause_publish_sensors':False })         

        if "tail lift" in command['body']:     
            if command['body'] == "tail lift down": value = "down"
            if command['body'] == "tail lift up":  value = "up"

            sensor_patch = {   'actuators':{
                                        'sensor_act1': {
                                            'title':"Tail Lift",
                                            'type' :"string",
                                            'value': value,
                                            'unit': ""}
                                        }
                        } 

        if "headlight" in command['body']:     
            if command['body'] == "headlight on": value = "on"
            if command['body'] == "headlight off":  value = "off"

            sensor_patch = {   'lights':{
                                        'sensor_hl1': {
                                            'title':"Headlight",
                                            'type' :"string",
                                            'value': value,
                                            'unit': ""}
                                        }
                        } 

            
        sensors = {**agent_data['sensors'], **sensor_patch}
        agent_data['sensors'] = sensors
        position_sensor_ros.publish(agent_data)   


    except Exception as e:
        print(e)