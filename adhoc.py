from lights import smart_plugs as smart_plugs
from sounds import speakers as speakers
from dotenv import load_dotenv
import time
import os

load_dotenv()

# print(smart_plugs.get_lights())
# # smart_plugs.turn_all_lights_off()
# print(smart_plugs.get_lights())
# # smart_plugs.turn_all_lights_on()

# smart_plugs.turn_all_lights_on()
# time.sleep(1)
# smart_plugs.turn_all_lights_off()
# time.sleep(1)
# smart_plugs.turn_all_lights_on()
# time.sleep(1)
# smart_plugs.turn_all_lights_off()

# speakers.list_audio_devices()
# speakers.set_device_by_name("JBL")
smart_plugs.turn_all_lights_off()
smart_plugs.turn_all_lights_on()
speakers.play_clue_solved_sound_effect()
time.sleep(1)
smart_plugs.turn_all_lights_off()