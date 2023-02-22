import openai

class OpenAIHandler:
    def __init__(self, api_key):
        """
        Initializes a new instance of the OpenAIHandler class.
        """
        self.api_key = api_key
        openai.api_key = api_key

    def get_response(self, content):
        """
        Sends a prompt to the OpenAI API and returns the generated response.
        """
        # The code below returns a response using OpenAI based on the message.content that will be passed
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=content,
            max_tokens=50,
        )
        return response

    def generate_default_scores(self):
        """
        Generates default scores for each category.
        """
        return {
            'grammar': 100
        }

    def get_message_score(self, content):
        """
        Processes the text and generates various scores on different categories.
        """

        return {
            'grammar': 1
        } # PLACEHOLDER RETURN VALUE