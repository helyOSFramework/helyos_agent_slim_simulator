

from helyos_agent_sdk.models import AssignmentCurrentStatus, AGENT_STATE, AgentCurrentResources, ASSIGNMENT_STATUS

def reserve_callback( vehi_state_ros, agentConnector, ch, sender, req_resources, msg_str, signature):
    print("=> reserve agent", req_resources)

    resources = AgentCurrentResources(operation_types_available = req_resources.operation_types_required,
                                      work_process_id           = req_resources.work_process_id,
                                      reserved                  = req_resources.reserved)
    
    vehi_state_ros.publish({**vehi_state_ros.read(),"agent_state": AGENT_STATE.READY})
    agentConnector.publish_state(status=AGENT_STATE.READY, resources=resources, assignment_status=None)
    print("<= agent reserved", resources)
    
    
def release_callback(vehi_state_ros, agentConnector, ch, sender, req_resources, msg_str, signature):
    print(" => release agent", req_resources)
    
    resources = AgentCurrentResources(operation_types_available = req_resources.operation_types_required,
                                      work_process_id           = req_resources.work_process_id,
                                      reserved                  = req_resources.reserved)
    
    vehi_state_ros.publish({**vehi_state_ros.read(),'agent_state': AGENT_STATE.FREE})
    agentConnector.publish_state(status=AGENT_STATE.FREE, resources=resources, assignment_status=None)   
    print(" <= agent released", resources)
    



def do_something_to_interrupt_assignment_operations(driving_operation_ros):
    operation_commands = driving_operation_ros.read()
    driving_operation_ros.publish({**operation_commands, 'CANCEL_DRIVING': True, 'PAUSE_ASSIGNMENT': False})


def cancel_assignm_callback(driving_operation_ros, current_assignment_ros, agentConnector, ch, server, inst_assignm_cancel, msg_str, signature):
    assignment_metadata = inst_assignm_cancel.metadata   
    assignm_data = current_assignment_ros.read()
    agentConnector.current_assignment = AssignmentCurrentStatus(id=assignm_data['id'], status=assignm_data['status'], result=assignm_data.get('result',{}))

    if assignment_metadata.id == agentConnector.current_assignment.id:
        do_something_to_interrupt_assignment_operations(driving_operation_ros)
        print(" * cancelling order dispatched")
    else:
        print("assignment id is not running in this agent")
        print("cancelling assignment:", assignment_metadata.id)
        print("current assignment:", agentConnector.current_assignment.id)
