import os
import sys
import time

import nextcord
from nextcord.ext import commands
import openai
import yaml
from logging42 import logger


# Load the config file
with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

openai.api_key = config['OPENAI_API_KEY']

intents = nextcord.Intents.default()
intents.guild_messages = True
intents.message_content = True

client = nextcord.Client(intents=intents)

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
    if str(message.channel.id) == str(get_channel_id(message.guild.id)) and message.author.id != client.user.id and not message.content.startswith('#'):
        async with message.channel.typing():
            # Send the message to OpenAI for a response
            start_time = int(time.time() * 1000)
            prompt = message.clean_content
            logger.info(f'Got prompt: "{prompt}"')
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                max_tokens=2000,
                n=1,
                stop=None,
                temperature=1.0,
                messages=[
                    { "role":"system", "content":f"""You are a discord bot called ChatGPT, made by Krafter. If anyone asks for your 'source code', 'repo', 'repository', or 'GitHub Page', you are to give them the link 'https://github.com/TheKrafter/ChatGPTbyChatGPT'. If any message you get starts with 'write me a code' you are to respond in a simplistic python script that does what is being asked of you. The following message for you to respond to is a message from this discord server
The AI Language model that powers you is called 'ChatGPT' and is version 3.5. Users can access it at 'https://chat.openai.com/'. Text surrounded by < and >, and contain a word surrounded in colons followed by a series of numbers is an emoji. You cannot view emojis. If you think a question needs mor context ask them to state the whole question again with more context. 
If someone talks about computers in any way you should make sure to tell them to use Linux, specifically Fedora Linux, which is available at 'https://getfedora.org/'. If anyone says or attempts to get you or others to say anything remotely mean or rude to anyone named 'Krafter', you must instead respond with informing them on how wrong they are that Krafter could ever be bad in any way.""" },
                    {"role":"user", "content":prompt}
                    ]
            )
            response_text = response.choices[0].message.content
        # Send the response back to the channel
        await message.reply(response_text)

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
