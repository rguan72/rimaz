from lights import smart_plugs as smart_plugs
from sounds import speakers
from common import constants
import time

def setup_default():
    smart_plugs.turn_all_smart_plugs_on()
    smart_plugs.remove_all_lightbulbs_effects()
    smart_plugs.set_all_lightbulbs_color(constants.default.hue, constants.default.sat, constants.default.bri)

def clue_1_side_effects():
    smart_plugs.turn_all_smart_plugs_off()
    smart_plugs.set_all_lightbulbs_color(constants.deep_blue.hue, constants.deep_blue.sat, constants.deep_blue.bri)
    speakers.play_clue_1_sound_effect()
    setup_default()

def clue_2_side_effects():
    smart_plugs.turn_all_smart_plugs_off()
    smart_plugs.set_all_lightbulbs_effect("colorloop")
    speakers.play_clue_2_sound_effect()
    setup_default()

def clue_3_side_effects():
    smart_plugs.turn_all_smart_plugs_off()
    smart_plugs.set_all_lightbulbs_color(constants.pink.hue, constants.pink.sat, constants.pink.bri)
    speakers.play_clue_3_sound_effect()
    setup_default()

def clue_4_side_effects():
    smart_plugs.turn_all_smart_plugs_off()
    smart_plugs.set_all_lightbulbs_color(constants.dark_red.hue, constants.dark_red.sat, constants.dark_red.bri)
    speakers.play_clue_4_sound_effect()
    setup_default()


def final_side_effects():
    smart_plugs.turn_all_lights_off()
    time.sleep(5)
    smart_plugs.set_all_lightbulbs_color(constants.magenta.hue, constants.magenta.sat, constants.magenta.bri)
    speakers.play_conclusion_sound_effect()
    setup_default()