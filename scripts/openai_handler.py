import openai


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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": content},
            ],
        )
        return response.choices[0]["message"]["content"]

    def generate_default_scores(self):
        """
        Generates default scores for each category.
        """
        return {"grammar": 100}

    def get_message_score(self, content):
        """
        Processes the text and generates various scores on different categories.
        """

        return {"grammar": self.get_grammar_score(content)}

    def get_grammar_score(self, content):
        with open(self.grammar_prompt_path, "r") as file:
            prompt = file.read()

        prompt += content

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                ],
            )

            grammar_score = response.choices[0]["message"]["content"]

            grammar_score = int(grammar_score)
            grammar_score = ((grammar_score / 5) - 1) * 10

            if grammar_score < -10 or grammar_score > 10:
                return -1001

        except openai.error.AuthenticationError:
            print("No API key provided")
            return -1001

        except ValueError:  # meaning API did not produce a pure number
            return -1001

        return grammar_score
