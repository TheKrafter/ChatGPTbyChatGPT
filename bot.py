import os
import sys
import time

import nextcord
from nextcord.ext import commands
import openai
import yaml
from logging42 import logger

# Only show "INFO" and higher
logger.add(sink=sys.stdout, level="INFO")

# Load the config file
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

openai.api_key = config['OPENAI_API_KEY']

intents = nextcord.Intents.default()
intents.messages = True

client = nextcord.Client()

# Define a function to save the channel ID to the storage.yml file
def save_channel_id(guild_id, channel_id):
    storage = {'guilds': {}}
    if os.path.exists('storage.yml'):
        with open('storage.yml', 'r') as f:
            storage = yaml.safe_load(f)
    storage['guilds'][str(guild_id)] = {'channel_id': str(channel_id)}
    with open('storage.yml', 'w') as f:
        yaml.dump(storage, f)

# Define a function to fetch the channel ID from the storage.yml file
def get_channel_id(guild_id):
    if os.path.exists('storage.yml'):
        with open('storage.yml', 'r') as f:
            storage = yaml.safe_load(f)
            return storage['guilds'].get(str(guild_id), {}).get('channel_id')

@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if str(message.channel.id) == str(get_channel_id(message.guild.id)) and message.author.id != client.user.id:
        # Send the message to OpenAI for a response
        start_time = int(time.time() * 1000)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=1.0,
            messages=[
                {"role":"system", "content":"You're a discord bot in a family-friendly, minecraft focused discord server."},
                {"role":"user", "content":message.content}
                ]
        )
        response_text = response.choices[0].text.strip()
        # Send the response back to the channel
        await message.channel.send(response_text)

        end_time = int(time.time() * 1000)
        logger.success(f'Responded to a prompt in {end_time - start_time}ms!')

# Define a slash command to set the channel ID
@client.slash_command(name='set_channel', description='Set the channel where the client listens for messages')
async def set_channel(ctx, channel: nextcord.TextChannel):
    if ctx.user.guild_permissions.administrator:
        save_channel_id(ctx.guild.id, channel.id)
        await ctx.send(f'Channel set to {channel.mention}!')
    else:
        await ctx.send('You must be an administrator to use this command.')

# Load the client token from the config file
client.run(config['DISCORD_BOT_TOKEN'])
