import time
from gpiozero import MotionSensor
import os
import json
import mysql.connector
import pyaudio
import wave
import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


def recordAudio():
    FORMAT = pyaudio.paInt32
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "go.wav"
     
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

def transcribeFile(fileName):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service-request.json"
    os.system("avconv -i " + fileName + ".wav -ac 1 " + fileName + ".flac")

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    file_name = os.path.join(
        os.path.dirname(__file__),
        fileName + '.flac')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    if response is None:
        output = ''

    for result in response.results:
        output = result.alternatives[0].transcript

    return output

def queryDatabase(output):
    cnx = mysql.connector.connect(user='mguay', password='ramsamsam123', host='localhost', database='safetypi')
    cursor = cnx.cursor()
    query = ("SELECT * FROM USERS;")
    cursor.execute(query)

    for id in cursor:
        for value in id:
            if str(value) == str(output):
                return True

    return False


def addUser(id):
    cnx = mysql.connector.connect(user='mguay', password='ramsamsam123', host='localhost', database='safetypi')
    cursor = cnx.cursor()

    add_user = ("INSERT INTO USERS (id) VALUES (" + str(id) + ")")

    cursor.execute(add_user)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

def textToSpeech(text):
    os.system("curl -H \"Authorization: Bearer \"$(gcloud auth application-default print-access-token) -H \"Content-Type: application/json; charset=utf-8\" --data \"{\'input\':{\'text\': \'" + text + "\'},\'voice\':{\'languageCode\':\'en-gb\',\'name\':\'en-GB-Standard-A\',\'ssmlGender\':\'FEMALE\'},\'audioConfig\':{\'audioEncoding\':\'MP3\'}}\" \"https://texttospeech.googleapis.com/v1beta1/text:synthesize\" > synthesize-output.json")

    with open('synthesize-output.json') as data_file:    
        data = json.load(data_file)

    content = data['audioContent']
    file = open("synthesize-output-base64.txt", "w+")
    file.write(content)
    file.close()

    os.system("base64 synthesize-output-base64.txt --decode > synthesized-audio.mp3")

    os.remove("synthesize-output.json")
    os.remove("synthesize-output-base64.txt")

    # Then play audio
    



def main():
    pir = MotionSensor(4)
    while True:
        count = 1
        authenticated = False
        if pir.motion_detected:
            while (authenticated == False):
                if (count == 4):
                    # Send text to admin
                    print("Intruder alert")
                    return

                print("Motion detected")
                recordAudio()
                output = transcribeFile("go")
                os.remove("go.wav")
                os.remove("go.flac")
                result = queryDatabase(output)
                if result:
                    # User has been authenticated
                    # Play authentication sound
                    print("Welcome")
                    authenticated = True
                    return
                else:
                    # Play incorrect code sound, let the user try again, max 3 times
                    print("Please try again")
                    count += 1
            
        else:
            print("No motion detected")

    # textToSpeech("hello")


main()