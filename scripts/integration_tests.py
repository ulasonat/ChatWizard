import discord
from discord_bot import DiscordBot
from openai_handler import OpenAIHandler

class TestIntegration:
    def setup(self):
        self.open_ai_api_key = os.getenv('OPENAI_KEY')
        self.discord_api_key = os.getenv('DISCORD_KEY')
        self.grammar_prompt_path = '../prompts/grammar.txt'

        self.openai_handler = OpenAIHandler(api_key=self.open_ai_api_key, grammar_prompt_path=self.grammar_prompt_path)
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.message_content = True

        self.bot = DiscordBot(intents=self.intents, openai_handler=self.openai_handler,
                              log_file_path='test_log.txt', user_scores_path='test_user_scores.json')

    async def test_integration(self):
        server = await self.bot.fetch_guild('test server id')
        test_user = await server.create_test_member()

        user_message = 'How are you feeling?'
        await self.bot.on_message(user_message, test_user)

        assert self.bot.last_message is not None

        scores = self.openai_handler.get_message_score(user_message)
        assert scores['grammar'] > 8.0