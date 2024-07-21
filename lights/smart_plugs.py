import requests
import common.constants as constants

def get_lights():
    response = requests.get(f'http://{constants.bridge_ip}/api/{constants.username}/lights')
    return response.json()
