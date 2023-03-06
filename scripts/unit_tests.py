import json
import os
import pytest
import discord
from faker import Faker
from unittest.mock import Mock, patch, MagicMock
from discord_bot import DiscordBot
from openai_handler import OpenAIHandler


@pytest.fixture
def bot():
    openai_handler = Mock()
    intents = discord.Intents.default()

    log_file_path = "test_log.txt"
    user_scores_path = "test_user_scores.json"
    bot = DiscordBot(
        intents=intents,
        openai_handler=openai_handler,
        log_file_path=log_file_path,
        user_scores_path=user_scores_path,
    )

    return bot


@pytest.fixture
def handler():
    handler = OpenAIHandler(api_key="test_key", grammar_prompt_path="test_path")
    return handler


def test_init(bot):
    test_intents = discord.Intents.default()
    test_openai_handler = Mock()
    test_log_file_path = "test_log.txt"
    test_user_scores_path = "test_user_scores.json"

    bot = DiscordBot(
        intents=test_intents,
        openai_handler=test_openai_handler,
        log_file_path=test_log_file_path,
        user_scores_path=test_user_scores_path,
    )

    assert bot.openai_handler == test_openai_handler
    assert bot.log_file_path == test_log_file_path
    assert bot.user_scores_path == test_user_scores_path


def test_scan_message(bot):
    message_from_bot = Mock(author=bot.user, content=Faker().text())
    message_from_user = Mock(author="user", content=Faker().text())

    assert not bot.scan_message(message_from_bot)
    assert bot.scan_message(message_from_user)


def test_save_updated_scores(bot):
    test_user_id = Faker().pyint()
    test_scores = {"grammar": 10}

    assert test_user_id not in bot.user_scores
    bot.user_scores[test_user_id] = test_scores
    bot.save_updated_scores(test_user_id, test_scores)
    assert bot.user_scores[test_user_id]["grammar"] == 20


def test_load_user_scores(bot):
    fake_id1 = Faker().text(max_nb_chars=5)
    fake_id2 = Faker().text(max_nb_chars=5)
    temp_user_scores = {fake_id1: {"grammar": 45}, fake_id2: {"grammar": 80}}
    with open("temp_user_scores.json", "w") as file:
        json.dump(temp_user_scores, file)

    bot.user_scores_path = "temp_user_scores.json"
    bot.user_scores = bot.load_user_scores()

    assert bot.user_scores[fake_id1]["grammar"] == 45
    assert bot.user_scores[fake_id2]["grammar"] == 80


def test_save_user_scores(bot):
    test_user_id = Faker().text(max_nb_chars=5)
    test_data = {test_user_id: {"grammar": 50}}

    assert test_user_id not in bot.user_scores

    bot.user_scores = test_data
    bot.save_user_scores()

    with open(bot.user_scores_path, "r") as file:
        test_scores = json.load(file)

    assert test_scores is not None


def test_update_log_file(bot):
    test_nickname = Faker().name()
    test_content = Faker().text()

    if os.path.exists(bot.log_file_path):
        os.remove(bot.log_file_path)

    bot.update_log_file(test_nickname, test_content)

    assert os.path.exists(bot.log_file_path)

    with open(bot.log_file_path, "r") as file:
        log_contents = file.read()

    assert log_contents is not None
    assert test_nickname + ": " + test_content in log_contents


def test_generate_default_scores(handler):
    test_data = handler.generate_default_scores()
    assert test_data == {"grammar": 100}


def test_get_grammar_score_invalid(handler):
    content = "I is going out"

    test_prompt = f"This is a test prompt\n\nQ: {content}\nA:"
    with open(handler.grammar_prompt_path, "w") as file:
        file.write(test_prompt)

    expected_score = -1001
    print(handler.get_grammar_score)
    assert handler.get_grammar_score(content) == expected_score
