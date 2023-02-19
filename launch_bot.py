import discord

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Logged in succesfully!')

@client.event
async def on_message(message):
    if message.content.startswith('chatwizard'): # if someone types chatwizard in the server
        await message.channel.send('Hello! How can I help?') # will respond to it

client.run('MTA3Njc3Mzk4ODY0NDE3MTgxNw.GBVeOP.VexZT68CxYWp0Rm-6pb77d5Dr2OJwFXD66jRWs')