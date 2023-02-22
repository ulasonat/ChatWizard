import os
import discord
from openai_handler import OpenAIHandler
from discord_bot import DiscordBot

open_ai_api_key = os.getenv('OPENAI_KEY')
discord_api_key = os.getenv('DISCORD_KEY')
log_file_path = '../log/log.txt'
user_scores_path = '../log/user_scores.txt'

openai_handler = OpenAIHandler(api_key=open_ai_api_key)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = DiscordBot(intents=intents, openai_handler=openai_handler, log_file_path=log_file_path, user_scores_path=user_scores_path)
bot.run(discord_api_key)
