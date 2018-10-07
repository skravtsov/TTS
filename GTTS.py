from google.cloud import texttospeech
from playsound import playsound
import os
import random
import string


class GTTS():

    def __init__(self):
        # init tts_client
        self.tts_client = texttospeech.TextToSpeechClient()


    # Set the text input to be synthesized
    def speak(text):
        synthesis_input = texttospeech.types.SynthesisInput(text=text)

        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code="en-US"
        ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        response = self.tts_client.synthesize_speech(synthesis_input, voice, audio_config)

        fname = os.getcwd() + '/tts-temp' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + '.mp3'

        # The response's audio_content is binary.
        out = open(fname, 'wb')
        # Write the response to the output file.
        out.write(response.audio_content)
        #print('Audio content written to file ' + fname)
        out.close()

        playsound(fname, True)
        os.remove(fname)
