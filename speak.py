#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import re
import sys
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.api_core.exceptions import OutOfRange
from MicrophoneStream import MicrophoneStream
from GTTS import GTTS
from dialogflow import DF_intents

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "/Vark-4c05c8d4b9c7.json"



class LangParams:
    def __init__(self, lang, locale, phrases):
        self.lang = lang
        self.locale = locale
        self.phrases = phrases

lang_en =  LangParams("en", "en-US", ["Wark", "Vark listen to me", "ukrainska",
                                                 "ukrajinska", "ukraine", "find box"
                                                "find the box", "find the bottle",
                                                 "find bottle"])
lang_ua =  LangParams("uk", "uk-UA", ["Варк", "Шукай бутилку", "шукай коробку","Варк, шукай бутилку"])

params=lang_en

def df_action( action):
    if (action == "lang_ua"):
        params = lang_ua
        # raise OutOfRange('Restart stream!')
    if (action == "lang_en"):
        params = lang_en


df = DF_intents("vark-6785b", "vark-1", df_action, debug=True)
tts = GTTS()



def listen_print_loop(responses):
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            df.detect_intent_texts([transcript],params.lang)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                exit(0)

            num_chars_printed = 0



def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.

    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms
    client = speech.SpeechClient()

    tts.speak("Okay, let me open stream!")

    while(True): #loop with streams
        try:
            language_code = params.locale  # a BCP-47 language tag


            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=RATE,
                language_code=language_code,
                speech_contexts=[
                    types.SpeechContext(phrases=params.phrases)
                ]
            )

            streaming_config = types.StreamingRecognitionConfig(
                config=config,
                interim_results=True)

            with MicrophoneStream(RATE, CHUNK) as stream:
                audio_generator = stream.generator()
                requests = (types.StreamingRecognizeRequest(audio_content=content)
                            for content in audio_generator)

                responses = client.streaming_recognize(streaming_config, requests)

                # Now, put the transcription responses to use.
                tts.speak("I'm ready. Say something!")
                listen_print_loop(responses)
        except OutOfRange:
            print("Stream restart")



if __name__ == '__main__':
    main()
# [END speech_transcribe_streaming_mic]