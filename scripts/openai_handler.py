import openai
import re

class OpenAIHandler:
    def __init__(self, api_key, grammar_prompt_path):
        """
        Initializes a new instance of the OpenAIHandler class.
        """
        self.api_key = api_key
        self.grammar_prompt_path = grammar_prompt_path
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
            'grammar': self.get_grammar_score(content)
        }

    def get_grammar_score(self, content):

        with open(self.grammar_prompt_path, 'r') as file:
            prompt = file.read()

        prompt += content

        grammar_score = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,
        )

        grammar_score = grammar_score.choices[0].text
        try:
            grammar_score = int(grammar_score)
            grammar_score = ((grammar_score / 5) - 1) * 10

            if grammar_score < -10 or grammar_score > 10:
                return -1001
        except:
            return -1001 # Error code, will be handled. CURRENTLY GETS CALLED TOO FREQUENTLY

        return grammar_score