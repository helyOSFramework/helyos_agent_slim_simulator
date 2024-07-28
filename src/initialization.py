import os, json, time
from helyos_agent_sdk import HelyOSClient, HelyOSMQTTClient, AgentConnector
from helyos_agent_sdk.models import AssignmentCurrentStatus, AGENT_STATE, AgentCurrentResources


# 1 - AGENT INITIALIZATION

def agent_initialization (  PROTOCOL,
                            RABBITMQ_HOST, 
                            RABBITMQ_PORT, 
                            RBMQ_USERNAME,
                            RBMQ_PASSWORD,
                            UUID, YARD_UID,
                            ENABLE_SSL,
                            CA_CERTIFICATE,
                            AGENT_OPERATIONS,
                            CHECKIN_MAX_ATTEMPTS,
                            agent_data):
    
    if PROTOCOL == "AMQP":   
        MessageBrokerClient = HelyOSClient
    if PROTOCOL == "MQTT":
        MessageBrokerClient = HelyOSMQTTClient
    

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

    initial_status = AGENT_STATE.FREE
    operations = AGENT_OPERATIONS.split(',')
    resources = AgentCurrentResources(operation_types_available=operations, work_process_id=None, reserved=False)
    assignment = AssignmentCurrentStatus(id=None, status=None, result={})

    ## 1.1 Instantiate main helyOS client - we create one RabbitMQ connection per helyos_client
    helyOS_client = MessageBrokerClient(RABBITMQ_HOST, RABBITMQ_PORT, uuid=UUID, enable_ssl=ENABLE_SSL, ca_certificate=CA_CERTIFICATE)
    attempts = 0; helyos_excep = None
    while attempts < CHECKIN_MAX_ATTEMPTS:
        try:
            if RBMQ_USERNAME and RBMQ_PASSWORD:
                helyOS_client.connect(RBMQ_USERNAME, RBMQ_PASSWORD)

            print(f"Check in, attempt {attempts+1} ...")
            helyOS_client.perform_checkin(yard_uid=YARD_UID, agent_data=agent_data, status=initial_status.value)
            break
        except Exception as e:
            attempts += 1
            helyos_excep = e
            time.sleep(2)
    if attempts == CHECKIN_MAX_ATTEMPTS:
        raise helyos_excep

    helyOS_client.get_checkin_result()
    print("\n connected to message broker")

    ## 1.2 Instantiate main Agent Connector  
    agentConnector = AgentConnector(helyOS_client)
    agentConnector.publish_state(initial_status, resources, assignment_status=assignment)

    return helyOS_client, agentConnector, {'sensors': initial_sensor, 'status': initial_status.value}

