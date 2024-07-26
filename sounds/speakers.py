import sounddevice as sd
import numpy as np
from pydub import AudioSegment

def list_audio_devices():
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(f"{idx}: {device['name']}")
        print(device)

def set_device_by_name(device_name):
    devices = sd.query_devices()
    for _, device in enumerate(devices):
        if device_name in device['name']:
            sd.default.device = device['name']
            print(f"Device set to: {device['name']}")
            return

def play_mp3(file_path):
    # Load the MP3 file
    audio = AudioSegment.from_file(file_path, format="mp3")
    # Convert to numpy array
    audio_data = np.array(audio.get_array_of_samples())
    # Play the audio data
    sd.default.device = "JBL Charge 3"
    sd.play(audio_data, audio.frame_rate)
    sd.wait()  # Wait until the file has finished playing

def play_voted_sound_effect():
    play_mp3("sounds/assets/clue_solved.mp3")

def play_clue_1_sound_effect():
    play_mp3("sounds/assets/clue_1.mp3")

def play_clue_2_sound_effect():
    play_mp3("sounds/assets/clue_2.mp3")

def play_clue_3_sound_effect():
    play_mp3("sounds/assets/clue_3.mp3")

def play_clue_4_sound_effect():
    play_mp3("sounds/assets/clue_4.mp3")

# Parameters for the inaudible sound
duration = 0.5  # seconds
frequency = 20  # Hz, low-frequency sound
sample_rate = 44100  # samples per second

def play_inaudible_sound():
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_signal = 0.001 * np.sin(2 * np.pi * frequency * t)  # Very low amplitude signal
    sd.default.device = "JBL Charge 3"
    sd.play(audio_signal, sample_rate)
    sd.wait()
