import requests
import common.constants as constants
import time

def get_lights():
    response = requests.get(f'http://{constants.bridge_ip}/api/{constants.username}/lights')
    return response.json()

def control_light(light_id, state, transitiontime=0):
    payload = {
        "on": state,
        "transitiontime": transitiontime,
    }
    response = requests.put(f'http://{constants.bridge_ip}/api/{constants.username}/lights/{light_id}/state', json=payload)
    return response.json()

def control_all_lights(state):
    lights = get_lights()
    for id, _ in lights.items():
        control_light(id, state)

def turn_all_lights_on():
    control_all_lights(True)

def turn_all_lights_off():
    control_all_lights(False)

def light_effect():
    lights = get_lights()
    for id, body in lights.items():
        is_lightbulb = "Hue color" in body["productname"]
        if is_lightbulb:
            set_lightbulb_color(id, 60, 100, 100)
            time.sleep(1)
            control_light(id, False)
            time.sleep(1)
            control_light(id, True)
            time.sleep(1)
            control_light(id, False)

def set_lightbulb_color(light_id, hue, sat, bri, transitiontime=0):
    payload = {
        "on": True,
        'hue': hue,
        'sat': sat,
        'bri': bri,
        'transitiontime': transitiontime,
    }
    response = requests.put(f"http://{constants.bridge_ip}/api/{constants.username}/lights/{light_id}/state", json=payload)
    return response.json()
