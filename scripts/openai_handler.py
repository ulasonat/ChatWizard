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
    
    