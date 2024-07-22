import sounddevice as sd

def list_audio_devices():
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print(f"{idx}: {device['name']}")