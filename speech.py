def transcribeFile(fileName):

    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

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
    for result in response.results:
        output = result.alternatives[0].transcript

    return output

def queryDatabase(output):
    import mysql.connector

    cnx = mysql.connector.connect(user='mguay', password='ramsamsam123', host='localhost', database='safetypi')
    cursor = cnx.cursor()
    query = ("SELECT * FROM USERS;")
    cursor.execute(query)

    for id in cursor:
        for value in id:
            if value == output:
                cursor.close()
                cnx.close()
                return True
                
    cursor.close()
    cnx.close()
    return False


def addUser(id):
    import mysql.connector

    cnx = mysql.connector.connect(user='mguay', password='ramsamsam123', host='localhost', database='safetypi')
    cursor = cnx.cursor()

    add_user = ("INSERT INTO USERS (id) VALUES (" + str(id) + ")")

    cursor.execute(add_user)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()


def main():
    output = transcribeFile("go")
    result = queryDatabase(output)

    if result:
        # User has been authenticated
        print("Welcome")
    else:
        print("Please try again")
        # Try again two more times

main()