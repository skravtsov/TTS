# Google STT - Dialogflow - Google TTS loop
Python Google Speech To Text API to Dialogflow to Google Text To Speech API

This class creates Listen Loop - listening user voice, converting to text with Google Cloud STT API, then process with Dialogflow, achieves a feedback and reading with Google Cloud TTS API

This is basically voice bot based on Dialog Flow

Tested on:
* Windows 10 x64
* Raspberry Pi 3



Usage
-----

```
from speak import  LangParams, ListenLoop


lang_en = LangParams("en", "en-US",
                     phrases = ["Wark", "Vark listen to me",
                      "ukrainska", "ukrajinska", "ukraine",
                      "find box", "find the box", "find the bottle","find bottle"],
                     start_phrase = "I'm ready! Talk to me"
                     )

def df_action(action):
    print("Action from DF:"+action)

listen =  ListenLoop(rate=16000,
                     project_id="vark-6785b",
                     df_action = df_action,
                     lang = lang_en,
                     device=2
                     )

while(True):
    listen.run()
```
