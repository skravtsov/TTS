from speak import  LangParams, ListenLoop


lang_en = LangParams("en", "en-US",
                     phrases = ["Wark", "Vark listen to me",
                      "ukrainska", "ukrajinska", "ukraine",
                      "find box", "find the box", "find the bottle","find bottle"],
                     start_phrase = "I'm ready! Talk to me"
                     )
lang_ua = LangParams("uk", "uk-UA",
                     phrases= ["Варк",
                               "Шукай бутилку", "шукай коробку", "Варк, шукай бутилку"],
                     start_phrase= "Ja gottov dopomohty")






def df_action(action):
    if (action == "lang_ua"):
        listen.change_lang(lang_ua)
        # raise OutOfRange('Restart stream!')
    if (action == "lang_en"):
        listen.change_lang(lang_en)


listen =  ListenLoop(rate=16000,
                     project_id="vark-6785b",
                     df_action = df_action,
                     lang = lang_en,
                     device=2
                     )

while(True):
    time.sleep(1)
    listen.run()