import sys
import discord
from openai_handler import OpenAIHandler
from discord_bot import DiscordBot


def run(open_ai_api_key, discord_api_key):
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
