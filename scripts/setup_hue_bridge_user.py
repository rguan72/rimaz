import requests
import json

# you must press link button on bridge before running this script
bridge_ip = "192.168.1.120"

payload = {
    "devicetype": "my_hue_app#my_laptop"
}

response = requests.post(f'http://{bridge_ip}/api', json=payload)

print(response)
print(response.text)

username = json.loads(response.text)[0]["success"]["username"]
print(username)