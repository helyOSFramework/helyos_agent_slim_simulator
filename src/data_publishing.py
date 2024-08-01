
import time, json, math, os
from helyos_agent_sdk import AgentConnector
from helyos_agent_sdk.models import AssignmentCurrentStatus

from customization.connected_tool_sensors import get_tool_position
GEOMETRY_FILENAME = os.environ.get('GEOMETRY_FILENAME', "customization/geometry.json")
UPDATE_RATE = int(os.environ.get('UPDATE_RATE', '2'))

try:
    with open(GEOMETRY_FILENAME) as f:
        GEOMETRY =json.load(f)
except:
    GEOMETRY = {0:None}


# These functions can be used to parse data

def get_vehicle_position(position_sensor_ros):
    # Get x, y, orientations from the vehicle
    return position_sensor_ros.read()


def get_assignment_state(current_assignment_ros):
    ''' Get vehicle state: "failed", "active", "succeeded", etc... '''    
    return current_assignment_ros.read()


def interprete_vehicle_state(vehicle_data, assignm_data, vehi_state_ros ): 
    ''' agent state ("free", "ready", "busy"...). '''
    return vehi_state_ros.read()




def periodic_publish_state_and_sensors(helyOS_client2, current_assignment_ros, vehi_state_ros, position_sensor_ros):
    agentConnector2 = AgentConnector(helyOS_client2)
    period = 1/UPDATE_RATE # second => default 2 Hz
    z=0; previous_status = None; previous_state = None
    time.sleep(2)

    while True:
        time.sleep(period)

        try: # SENSORS AND  POSITIONS - VISUALIZATION CHANNEL - HIGH FREQUENCY
            if not vehi_state_ros.read().get('pause_publish_sensors', False):
                # Publish truck position
                try:
                    agent_data = get_vehicle_position(position_sensor_ros)
                    agentConnector2.publish_sensors(x=agent_data["x"], y=agent_data["y"], z=0,
                                                    orientations=agent_data['orientations'], sensors=agent_data['sensors'], signed=False)
                except Exception as e:
                    print("cannot read truck position.", e)

                # Publish trailer position
                try:
                    trailer = vehi_state_ros.read().get('CONNECTED_TRAILER', None)
                except:
                    trailer = None

                if trailer is not None:
                    try:
                        truck_geometry = GEOMETRY[0]
                        trailer_data = get_tool_position(position_sensor_ros, truck_geometry)
                        body = trailer_data
                        message= json.dumps({'type': 'agent_sensors','body': body})
                        helyOS_client2.publish(routing_key=f"agent.{trailer['uuid']}.visualization", message=message)

                        
                    except Exception as e:
                        print("cannot read connected tool position.", e)
        except:
            pass    

       
        try:  # ASSIGNMENT AND AGENT STATE - STATE AND UPDATE CHANNEL - LOW FREQUENCY  
            agent_data = get_vehicle_position(position_sensor_ros)
            assignm_data = get_assignment_state(current_assignment_ros)
            vehicle_data = interprete_vehicle_state(agent_data, assignm_data, vehi_state_ros)     
            assign_status_changed = assignm_data and (assignm_data['status'] != previous_status)
            agent_state_changed = vehicle_data and (vehicle_data['agent_state'] != previous_state)
            did_any_status_change = assign_status_changed or agent_state_changed

            if did_any_status_change:
                 # Publish agent and assignment statuses if they changed.
                agentConnector2.publish_state(status=vehicle_data['agent_state'], 
                                    assignment_status=AssignmentCurrentStatus(  id=assignm_data['id'], 
                                                                                status=assignm_data['status'],
                                                                                result=assignm_data.get('result',{})),
                                                                                signed=True)
             
                # Aditionally save the current position to the database with the minimum of latency.
                agentConnector2.publish_general_updates({'x':agent_data["x"], 'y':agent_data["y"], 'orientations': agent_data['orientations']}, signed=True)


                if trailer is not None:
                    try:
                        truck_geometry = GEOMETRY[0]
                        trailer_data = get_tool_position(position_sensor_ros, truck_geometry)
                        body = trailer_data
                        message= json.dumps({'type': 'agent_state','body': {'status':trailer['status']}})
                        helyOS_client2.publish(routing_key=f"agent.{trailer['uuid']}.state", message=message)
                    except Exception as e:
                        print("cannot read trailer state.", e)
                        

                previous_status =  assignm_data['status']   
                previous_state =  vehicle_data['agent_state']   


        except Exception as e:
            print("cannot read states.", e)