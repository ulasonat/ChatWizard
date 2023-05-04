"""
This script contains the implementation of the DiscordBot class, which is responsible for interacting with the
Discord API and OpenAI's GPT-3.5-turbo API to analyze and score members' behavior based on different categories.
"""

import discord
import os
import json


class DiscordBot(discord.Client):
    """
    A class that represents a Discord bot that encourages positivity
    within a server by analyzing and scoring each member's behavior.
    """

    def __init__(self, intents, openai_handler, log_file_path, user_scores_path):
        """
        Initializes a new instance of the DiscordBot class.

        Parameters:
            intents (discord.Intents): The intents of the discord client.
            openai_handler (OpenAIHandler): The OpenAI API handler for the bot.
            log_file_path (str): The log file path to store logs.
            user_scores_path (str): The user scores file path to store user scores.
        """

        super().__init__(intents=intents)
        self.openai_handler = openai_handler
        self.log_file_path = log_file_path
        self.user_scores_path = user_scores_path
        self.user_scores = self.load_user_scores()
        self.categories = ['grammar', 'friendliness', 'humor']

    async def on_ready(self):
        """
        A callback method that is called when bot connects to Discord.
        It prints a message to the console indicating that the bot has connected to Discord.
        """

        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        """
        A callback method that is called when the bot receives a message from a user.
        It processes the text and generates scores on categories such as grammar, friendliness, and humor, and
        responds with the scores and the appropriate label.

        Parameters:
            message (discord.Message): The message recieved from the discord server.
        """

        if not self.scan_message(message):
            return

        self.update_log_file(message.author, message.content)

        if message.content.startswith("!help"):
            embed = discord.Embed(
                title="Help on the way!",
                url="https://realdrewdata.medium.com/",
                description="**!help:** To get help\n**!me:**" " To see your stats" "\n**!reset:" "** Reset your stats",
                color=discord.Color.blue(),
            )

            await message.channel.send(embed=embed)

        elif message.content.startswith("!me"):
            if str(message.author.id) not in self.user_scores:
                embed = discord.Embed(
                    title="Failure :(",
                    url="https://realdrewdata.medium.com/",
                    description="Sorry, I couldn't find your scores.",
                    color=discord.Color.red(),
                )

                await message.channel.send(embed=embed)
            else:
                self.user_scores = self.load_user_scores()
                particular_scores = self.user_scores[str(message.author.id)]
                text = (
                    f"Grammar:** {particular_scores['grammar']}**\n"
                    f"Friendliness:** {particular_scores['friendliness']}"
                    f"**\nHumor:** {particular_scores['humor']}**"
                )

                embed = discord.Embed(
                    title="Here are your scores!",
                    url="https://realdrewdata.medium.com/",
                    description=text,
                    color=discord.Color.blue(),
                )

                await message.channel.send(embed=embed)

        elif message.content.startswith("!reset"):
            default_scores = self.openai_handler.generate_default_scores()
            self.user_scores[message.author.id] = default_scores
            self.save_user_scores()

            embed = discord.Embed(
                title="Success!",
                url="https://realdrewdata.medium.com/",
                description="**Your scores have reset!**",
                color=discord.Color.blue(),
            )

            await message.channel.send(embed=embed)

        else:
            scores = self.openai_handler.get_message_score(message.content)
            final_text = str()
            for label, score in scores.items():
                if not score == -1001:
                    results = label.capitalize() + ": **" + self.get_corresponding_word(label, score) + "**\n"
                    final_text += results
                else:
                    scores[label] = 0
                    text = label.capitalize() + ":**" + " Not calculated\n**"
                    final_text += text

            self.update_scores(message.author.id, scores)

            embed = discord.Embed(
                title=message.content,
                url="https://realdrewdata.medium.com/",
                description=final_text,
                color=discord.Color.blue(),
            )

            await message.channel.send(embed=embed)

    def scan_message(self, message):
        """
        Returns `True` if the message was sent by a user,
        and `False` otherwise, and prints the message

        Parameters:
            message (discord.Message): The message recieved from the discord server.

        Returns:
            bool: Whether the message was sent by a user or not.
        """
        if message.author == self.user:
            return False

        return True

    def update_scores(self, user_id, scores):
        """
        Updates the scores of the given user ID with the
        scores from the most recent message they sent.

        Parameters:
            user_id (str): The user id whose scores needs to be updated.
            scores (dict): A dictionary containing scores on different categories.
        """
        if user_id not in self.user_scores:
            self.user_scores[user_id] = self.openai_handler.generate_default_scores()

        self.save_updated_scores(user_id, scores)

    def save_updated_scores(self, user_id, scores):
        """
        Updates the scores for the given user ID with the scores from the most recent message sent by the user.

        Parameters:
            user_id (str): Unique ID of the user whose scores are being updated.
            scores (dict): A dictionary containing the updated scores for the user.
        """
        self.user_scores[user_id]["grammar"] += scores["grammar"]
        self.user_scores[user_id]["friendliness"] += scores["friendliness"]
        self.user_scores[user_id]["humor"] += scores["humor"]
        self.save_user_scores()

    def load_user_scores(self):
        """
        Loads the user scores from the JSON file.

        Returns:
            dict: A dictionary that maps user IDs to their scores.
        """
        if not os.path.exists(self.user_scores_path):
            return {}

        with open(self.user_scores_path, "r") as file:
            return json.load(file)

    def save_user_scores(self):
        """
        Saves the user scores to the JSON file by writing the self.user_scores dictionary to the JSON file.
        """

        with open(self.user_scores_path, "w") as file:
            json.dump(self.user_scores, file)

    def update_log_file(self, nickname, content):
        """
        Appends the nickname and message content to the log file.
        If the log file does not exist, creates a new log file.

        Parameters:
            nickname (str): The nickname of the user who sent the message.
            content (str): The content of the message.
        """

        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w") as log_file:
                log_file.write("Log file created.\n")

        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"{nickname}: {content}\n")

    def score_to_word(self, score_map, score):
        """
        Returns the corresponding word for a given score from the provided score map.

        Parameters:
            score_map (dict): The dictionary containing the score-word mapping.
            score (int): The score in the range [-1, 0, 1].

        Returns:
            str: The corresponding word for the score in the score map.
        """
        if score in score_map:
            return score_map[score]
        else:
            raise ValueError("Invalid score.")

    def get_corresponding_word(self, label, score):
        """
        Returns the corresponding word for a given score and label.

        Parameters:
            label (str): The label/category for the score.
            score (int): The score in the range [-1,0,1].

        Returns:
            str: The corresponding word for the score and label.

        Raises:
            ValueError: If label or score are not recognized or invalid.
        """
        valid_labels = ['grammar', 'friendliness', 'humor']
        words = {
            'grammar': {1: 'Appropriate', 0: 'Mediocre', -1: 'Bad'},
            'friendliness': {1: 'Friendly', 0: 'Natural', -1: 'Not friendly'},
            'humor': {1: 'Funny', 0: 'Mediocre', -1: 'Not funny'},
        }

        if label not in valid_labels:
            raise ValueError("Invalid label.")

        return self.score_to_word(words[label], score)
