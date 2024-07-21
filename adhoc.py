from lights import smart_plugs as smart_plugs
from dotenv import load_dotenv
import os

load_dotenv()

print(smart_plugs.get_lights())
