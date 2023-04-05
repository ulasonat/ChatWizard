"""
This script is responsible for running the ChatWizard Discord bot. It takes in two command line arguments:
    1. OpenAI API key
    2. Discord API key

This script runs the Discord client by initializing an instance of the DiscordBot class and passing it the appropriate
arguments. It initializes a new instance of the OpenAIHandler class and passes the necessary API key and prompts for
processing the text and generating various scores on different categories.
"""

import sys
import discord
from openai_handler import OpenAIHandler
from discord_bot import DiscordBot


def run(open_ai_api_key, discord_api_key):
    """
    Initializes instances of the OpenAIHandler and DiscordBot classes, and runs the Discord bot.

    Parameters:
        open_ai_api_key: A string representing the API key for OpenAI's GPT-3.5-turbo model.
        discord_api_key: A string representing the API key for the Discord bot.

    Return:
        None

    Side Effects:
        Initializes instances of the OpenAIHandler and DiscordBot classes.
        Runs the Discord bot using the provided Discord API key.

    Exceptions:
        Raises a DiscordException if the Discord bot login is unsuccessful.
    """
    try:
        log_file_path = "log/log.txt"
        user_scores_path = "json/user_scores.json"
        grammar_prompt_path = "prompts/grammar.txt"
        friendliness_prompt_path = "prompts/friendliness.txt"
        humor_prompt_path = "prompts/humor.txt"

        openai_handler = OpenAIHandler(
            api_key=open_ai_api_key,
            grammar_prompt_path=grammar_prompt_path,
            friendliness_prompt_path=friendliness_prompt_path,
            humor_prompt_path=humor_prompt_path,
        )
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        bot = DiscordBot(
            intents=intents,
            openai_handler=openai_handler,
            log_file_path=log_file_path,
            user_scores_path=user_scores_path,
        )

        if discord_api_key and openai_handler:
            bot.run(discord_api_key)

    except discord.errors.LoginFailure:
        print('Login unsuccessful')
        raise discord.errors.DiscordException


def main():
    open_ai_api_key = sys.argv[1]
    discord_api_key = sys.argv[2]
    run(open_ai_api_key, discord_api_key)


if __name__ == "__main__":
    main()
