import unittest
import discord
import json
import os
from faker import Faker
from unittest.mock import Mock, patch, MagicMock
from discord.ext import commands
from discord_bot import DiscordBot

class TestDiscordBot(unittest.TestCase):

    def setUp(self):
        self.openai_handler = MagicMock()
        self.faker = Faker()
        self.intents = discord.Intents.default()
        self.log_file_path = 'test_log.txt'
        self.user_scores_path = 'test_user_scores.json'
        self.bot = DiscordBot(intents=self.intents, openai_handler=self.openai_handler,
                              log_file_path=self.log_file_path, user_scores_path=self.user_scores_path)


    def test_init(self):
        test_intents = discord.Intents.default()
        test_openai_handler = MagicMock()
        test_log_file_path = self.faker.file_extension()
        test_user_scores_path = self.faker.file_extension()

        test_bot = DiscordBot(intents=test_intents, openai_handler=test_openai_handler,
                              log_file_path=test_log_file_path, user_scores_path=test_user_scores_path)

        self.assertEqual(test_bot.openai_handler, test_openai_handler)
        self.assertEqual(test_bot.log_file_path, test_log_file_path)
        self.assertEqual(test_bot.user_scores_path, test_user_scores_path)

    def test_scan_message(self):
        message_from_bot = Mock(author=self.bot.user, content=self.faker.text())
        message_from_user = Mock(author='user', content=self.faker.text())

        self.assertFalse(self.bot.scan_message(message_from_bot))
        self.assertTrue(self.bot.scan_message(message_from_user))

    def test_save_updated_scores(self):
        test_user_id = self.faker.pyint()
        test_scores = {'grammar': 10}

        self.assertNotIn(test_user_id, self.bot.user_scores)
        self.bot.user_scores[test_user_id] = test_scores
        self.bot.save_updated_scores(test_user_id, test_scores)
        self.assertEqual(self.bot.user_scores[test_user_id]['grammar'], 20)

    def test_load_user_scores(self):

        fake_id1 = self.faker.text(max_nb_chars=5)
        fake_id2 = self.faker.text(max_nb_chars=5)
        temp_user_scores = {fake_id1: {'grammar': 45}, fake_id2: {'grammar': 80}}
        with open('temp_user_scores.json', 'w') as file:
            json.dump(temp_user_scores, file)

        self.bot.user_scores_path = 'temp_user_scores.json'
        self.bot.user_scores = self.bot.load_user_scores()

        self.assertEqual(self.bot.user_scores[fake_id1]['grammar'], 45)
        self.assertEqual(self.bot.user_scores[fake_id2]['grammar'], 80)

    def test_save_user_scores(self):
        test_user_id = self.faker.text(max_nb_chars=5)
        test_data = {test_user_id: {'grammar': 50}}

        self.assertNotIn(test_user_id, self.bot.user_scores)

        self.bot.user_scores = test_data
        self.bot.save_user_scores()

        with open(self.user_scores_path, 'r') as file:
            test_scores = json.load(file)

        self.assertNotEqual(test_scores, None)

    def test_update_log_file(self):
        test_nickname = self.faker.name()
        test_content = self.faker.text()

        if os.path.exists(self.bot.log_file_path):
            os.remove(self.bot.log_file_path)

        self.bot.update_log_file(test_nickname, test_content)

        self.assertTrue(os.path.exists(self.bot.log_file_path))

        with open(self.bot.log_file_path, 'r') as file:
            log_contents = file.read()

        self.assertNotEqual(log_contents, None)
        self.assertIn(test_nickname + ": " + test_content, log_contents)


if __name__ == '__main__':
    unittest.main()
