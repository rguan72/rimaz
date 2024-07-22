import requests
import common.constants as constants

def get_lights():
    response = requests.get(f'http://{constants.bridge_ip}/api/{constants.username}/lights')
    return response.json()

def control_smart_plug(light_id, state):
    payload = {
        "on": state
    }
    response = requests.put(f'http://{constants.bridge_ip}/api/{constants.username}/lights/{light_id}/state', json=payload)
    return response.json()

def control_all_lights(state):
    lights = get_lights()
    for id, body in lights.items():
        is_plug = body["productname"] == "Hue smart plug"
        if is_plug:
            control_smart_plug(id, state)

def turn_all_lights_on():
    control_all_lights(True)

def turn_all_lights_off():
    control_all_lights(False)