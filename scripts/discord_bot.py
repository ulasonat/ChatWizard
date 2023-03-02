import discord
import os
import json

class DiscordBot(discord.Client):

    def __init__(self, intents, openai_handler, log_file_path, user_scores_path):
        """
        Initializes a new instance of the DiscordBot class.
        """

        super().__init__(intents=intents)
        self.openai_handler = openai_handler
        self.log_file_path = log_file_path
        self.user_scores_path = user_scores_path
        self.user_scores = self.load_user_scores()

    async def on_ready(self):
        """
        A callback method that is called when the bot connects to the Discord API.
        Prints a message to the console indicating that the bot has connected to Discord.
        """

        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        """
        A callback method that is called when the bot receives a message from a user.
        """

        if not self.scan_message(message):
            return

        if message.content.startswith('!help'):
            await message.channel.send('Here, I will provide guidance on how to get the most out this bot.')

        self.update_log_file(message.author, message.content)

        scores = self.openai_handler.get_message_score(message.content)
        for label, score in scores.items():
            if not score == -1001:
                await message.channel.send(label.capitalize() + ' score: ' + str(score))
            else:
                scores[label] = 0
                await message.channel.send('Something went wrong, your score remained the same.')

        self.update_scores(message.author.id)

    def scan_message(self, message):
        """
        Returns `True` if the message was sent by a user, and `False` otherwise, and prints the message
        """
        if message.author == self.user:
            return False

        return True

    def update_scores(self, user_id):
        """
        Updates the scores of the given user ID with the scores from the most recent message they sent
        """
        if user_id not in self.user_scores:
            self.user_scores[user_id] = self.openai_handler.generate_default_scores()

        self.save_updated_scores(user_id, scores)

    def save_updated_scores(self, user_id, scores):
        """
        Saves the updated scores
        """
        self.user_scores[user_id]['grammar'] += scores['grammar']
        self.save_user_scores()

    def load_user_scores(self):
        """
        Loads the user scores from the JSON file.
        Returns a dictionary that maps user IDs to their scores.
        """
        if not os.path.exists(self.user_scores_path):
            return {}

        with open(self.user_scores_path, 'r') as file:
            return json.load(file)

    def save_user_scores(self):
        """
        Saves the user scores to the JSON file.
        """
        with open(self.user_scores_path, 'w') as file:
            json.dump(self.user_scores, file)

    def update_log_file(self, nickname, content):
        """
        Appends the nickname and message content to the log file.
        If the log file does not exist, creates a new log file.
        """

        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as log_file:
                log_file.write('Log file created.\n')

        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f'{nickname}: {content}\n')
