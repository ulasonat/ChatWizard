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

        if message.content.startswith('chatwizard'):
            await message.channel.send('Hello! How can I help?')

        print(f'{message.author}: {message.content}')
        self.update_log_file(message.author, message.content)

        response = self.openai_handler.get_response(message.content) # for testing only, will be deleted
        print(response) # for testing only, will be deleted

        scores = self.openai_handler.get_message_score(message.content)
        user_id = str(message.author.id)

        if user_id not in self.user_scores:
            print(user_id, ' ', type(user_id))
            self.user_scores[user_id] = self.openai_handler.generate_default_scores()
            
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
