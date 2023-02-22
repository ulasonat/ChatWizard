import discord
import os

class DiscordBot(discord.Client):

    def __init__(self, intents, openai_handler, log_file_path):
        """
        Initializes a new instance of the DiscordBot class.
        """

        super().__init__(intents=intents)
        self.openai_handler = openai_handler
        self.log_file_path = log_file_path

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

        response = self.openai_handler.get_response(message.content)
        print(response)

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
