import discord
import os
import openai

open_ai_api_key = os.getenv('OPENAI_KEY')
discord_api_key = os.getenv('DISCORD_KEY')


openai.api_key = open_ai_api_key

log_file_path = '../log/log.txt'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

def update_log_file(nickname, content):
    # Create a log file if it does not exist
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as log_file:
            log_file.write('Log file created.\n')

    # Append the nickname and content to the file
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'{nickname}: {content}\n')

def get_openai_response(content):
    # The code below returns a response using OpenAI based on the message.content that will be passed
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=content,
        max_tokens=50,
    )

    return response

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith('chatwizard'): # if someone types "chatwizard" in the server
        await message.channel.send('Hello! How can I help?') # will respond to it

    print(f'{message.author}: {message.content}')
    update_log_file(message.author, message.content)

    response = get_openai_response(message.content) # feeding in the user input
    print(response) # printing the response by OpenAI

client.run(discord_api_key)
