import random

def get_agent_sensors(position_sensor_ros):
    sensors = {
                        'temperatures':{
                            'sensor_t1': {
                                'title':"cabine",
                                'type' :"number",
                                'value':random.randint(20,40),
                                'unit': "oC"}
                                },
                        "agent": {
                            "SoC": {
                                "title": "HV Battery SoC",
                                "type": "number",
                                "description": "Battery state of charge of HV System",
                                "unit": "%",
                                "minimum": 0,
                                "maximum": 100,
                                "value": random.randint(20,60)
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
                                "value": random.randint(20,80)
                            }
                        }
                       
                }
    

    return sensors