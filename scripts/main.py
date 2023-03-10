import os
import discord
from openai_handler import OpenAIHandler
from discord_bot import DiscordBot

open_ai_api_key = os.getenv("OPENAI_KEY")
discord_api_key = os.getenv("DISCORD_KEY")
log_file_path = "log/log.txt"
user_scores_path = "json/user_scores.json"
grammar_prompt_path = "prompts/grammar.txt"

openai_handler = OpenAIHandler(api_key=open_ai_api_key, grammar_prompt_path=grammar_prompt_path)
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
