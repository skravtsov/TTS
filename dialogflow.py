import dialogflow_v2 as dialogflow
from GTTS import GTTS

class DF_intents:

    def __init__(self, project_id, session_id, action_func,debug=False):
        self.project_id = project_id
        self.session_id = session_id
        self.action_func=action_func
        self.tts = GTTS()
        self.debug=debug

    def detect_intent_texts(self,texts, language_code, speak = True):
        """Returns the result of detect intent with texts as inputs.
        Using the same `session_id` between requests allows continuation
        of the conversaion."""

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.project_id, self.session_id)

        for text in texts:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(
                session=session, query_input=query_input)

            if self.debug:
                print('Detected intent: {} (confidence: {})\n'.format(
                    response.query_result.intent.display_name,
                    response.query_result.intent_detection_confidence))
                print('Fulfillment text: {}\n'.format(
                    response.query_result.fulfillment_text))
                print('Action text: {}\n'.format(
                    response.query_result.action))
               # print(response.query_result)
            if response.query_result.fulfillment_text != "" and speak:
                self.tts.speak(response.query_result.fulfillment_text)
            if (response.query_result.action != ""): #do_action
                self.action_func(action = response.query_result.action)



