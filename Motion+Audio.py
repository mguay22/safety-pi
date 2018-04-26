import time
from gpiozero import MotionSensor

#Imports for pyaudio
import pyaudio
import wave


def recordAudio():
    FORMAT = pyaudio.paInt32
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
    print("finished recording")
     
     
    # stop Recordings
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

pir = MotionSensor(4)

count=0
while True:
	if pir.motion_detected:
		print("Motion Detected", count)
		recordAudio()
		incrementCentralPopulation()
		time.sleep(2)
	else:
            print("No Motion Detected")



