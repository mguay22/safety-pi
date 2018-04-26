import time
# Use Cloudant to create a Cloudant client using account
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
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


def incrementCentralPopulation():
    username='3e6d30ee-d974-4ed8-a6b7-1504c9b01df6-bluemix'
    password = "72d189c906f2630a7793ac0918894d55ed07904548da1ca6ae4f274cacf7aa00"
    URL="https://3e6d30ee-d974-4ed8-a6b7-1504c9b01df6-bluemix:72d189c906f2630a7793ac0918894d55ed07904548da1ca6ae4f274cacf7aa00@3e6d30ee-d974-4ed8-a6b7-1504c9b01df6-bluemix.cloudant.com"

    client = Cloudant(username,password,url=URL)

    client.connect()
    dbname='codefest-info'
    db=client[dbname]
    '''
    results=Result(db.all_docs, include_docs=True)
    print ("Retrieved minimal document:\n{0}\n".format(results[0]))
    '''

    '''
    # First retrieve the document
    grundle = db['089061c18a884da9a718b16b76807712']
    grundle['currentTotal'] += 1
    # You must save the document in order to update it on the database
    grundle.save()
    '''

    # First retrieve the document
    central = db['59b03acc7eedb2b21639ff88f15a671e']
    central['currentTotal'] += 1
    # You must save the document in order to update it on the database
    central.save()


    '''
    session = client.session()
    database= client["codefest-info"]
    '''

    # Disconnect from the server
    client.disconnect()

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



