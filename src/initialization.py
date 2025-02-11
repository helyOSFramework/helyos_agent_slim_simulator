import time
from helyos_agent_sdk import HelyOSClient, HelyOSMQTTClient, AgentConnector
from helyos_agent_sdk.models import AssignmentCurrentStatus, AGENT_STATE, AgentCurrentResources


# 1 - AGENT INITIALIZATION

def agent_initialization (  rabbitmq_config,
                            agent_data,
                            UUID, YARD_UID,
                            AGENT_OPERATIONS,
                            CHECKIN_MAX_ATTEMPTS
                            ):
    

    
    if rabbitmq_config['protocol'] == "AMQP":   
        MessageBrokerClient = HelyOSClient
    if rabbitmq_config['protocol'] == "MQTT":
        MessageBrokerClient = HelyOSMQTTClient


    initial_status = AGENT_STATE.FREE

    ## 1.1 Instantiate main helyOS client - we create one RabbitMQ connection per helyos_client
    helyOS_client = MessageBrokerClient(rabbitmq_config['host'], 
                                        rabbitmq_config['port'], 
                                        uuid=UUID, enable_ssl= rabbitmq_config['enable_ssl'],
                                        ca_certificate=rabbitmq_config['ca_certificate'],
                                        vhost=rabbitmq_config['vhost'])
    attempts = 0; helyos_excep = None
    while attempts < CHECKIN_MAX_ATTEMPTS:
        print(f" Check in, attempt {attempts + 1} ...")
        try:
            if rabbitmq_config['username'] and rabbitmq_config['password']:
                helyOS_client.connect(rabbitmq_config['username'], rabbitmq_config['password'])

            helyOS_client.perform_checkin(yard_uid=YARD_UID, agent_data=agent_data, status=initial_status.value)

            break
        except Exception as e:
            print(e)

        attempts += 1
        time.sleep(2)

    if attempts == CHECKIN_MAX_ATTEMPTS:
        print("Check in exceeded maximum attempts, no connection to server.")
        exit(1)


    helyOS_client.get_checkin_result()
    print("\n connected to message broker")       
    

    ## 1.2 Instantiate main Agent Connector  
    agent_connector = AgentConnector(helyOS_client)
    operations = AGENT_OPERATIONS.split(',')
    resources = AgentCurrentResources(operation_types_available=operations, work_process_id=None, reserved=False)
    assignment = AssignmentCurrentStatus(id=None, status=None, result={})
    agent_connector.publish_state(initial_status, resources, assignment_status=assignment)


    return helyOS_client, agent_connector
