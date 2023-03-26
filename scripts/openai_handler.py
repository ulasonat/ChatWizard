import openai


class OpenAIHandler:
    def __init__(self, api_key, grammar_prompt_path, friendliness_prompt_path, humor_prompt_path):
        """
        Initializes a new instance of the OpenAIHandler class.
        """
        self.api_key = api_key
        self.grammar_prompt_path = grammar_prompt_path
        self.friendliness_prompt_path = friendliness_prompt_path
        self.humor_prompt_path = humor_prompt_path

        openai.api_key = api_key

    def get_response(self, content):
        """
        Sends a prompt to the OpenAI API and returns the generated response.
        """
        # The code below returns a response using
        # OpenAI based on the message.content that will be passed
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": content},
            ],
        )
        return response.choices[0]["message"]["content"]

    def generate_default_scores(self):
        """
        Generates default scores for each category.
        """
        return {"grammar": 10, "friendliness": 10, "humor": 10}

    def get_message_score(self, content):
        """
        Processes the text and generates various
         scores on different categories.
        """

        return {
            "grammar": self.get_grammar_score(content),
            "friendliness": self.get_friendliness_score(content),
            "humor": self.get_humor_score(content),
        }

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

        if grammar_score <= 0:
            return -1
        if grammar_score == 0:
            return 0
        if grammar_score >= 0:
            return 1

    def get_friendliness_score(self, content):
        with open(self.friendliness_prompt_path, "r") as file:
            prompt = file.read()

        prompt += content

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                ],
            )

            friendliness_score = response.choices[0]["message"]["content"]

            friendliness_score = int(friendliness_score)
            friendliness_score = ((friendliness_score / 5) - 1) * 10

            if friendliness_score < -10 or friendliness_score > 10:
                return -1001

        except openai.error.AuthenticationError:
            print("No API key provided")
            return -1001

        except ValueError:  # meaning API did not produce a pure number
            return -1001

        if friendliness_score <= 0:
            return -1
        if friendliness_score == 0:
            return 0
        if friendliness_score >= 0:
            return 1

    def get_humor_score(self, content):
        with open(self.humor_prompt_path, "r") as file:
            prompt = file.read()

        prompt += content

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                ],
            )

            humor_score = response.choices[0]["message"]["content"]

            humor_score = int(humor_score)
            humor_score = ((humor_score / 5) - 1) * 10

            if humor_score < -10 or humor_score > 10:
                return -1001

        except openai.error.AuthenticationError:
            print("No API key provided")
            return -1001

        except ValueError:  # meaning API did not produce a pure number
            return -1001

        if humor_score <= 0:
            return -1
        if humor_score == 0:
            return 0
        if humor_score >= 0:
            return 1
