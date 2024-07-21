from lights import smart_plugs as smart_plugs
from dotenv import load_dotenv
import os

load_dotenv()

print(smart_plugs.get_lights())
smart_plugs.turn_all_lights_off()
print(smart_plugs.get_lights())

