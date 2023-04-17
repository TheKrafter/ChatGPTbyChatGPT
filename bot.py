import os
import nextcord
from nextcord.ext import commands
import openai
import yaml
from dotenv import load_dotenv

load_dotenv()  # Load the .env file containing your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

bot = commands.Bot(command_prefix='!')

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

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.channel.id == get_channel_id(message.guild.id):
        # Send the message to OpenAI for a response
        response = openai.Completion.create(
            engine='davinci',
            prompt=message.content,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response_text = response.choices[0].text.strip()
        # Send the response back to the channel
        await message.channel.send(response_text)

# Define a slash command to set the channel ID
@bot.slash_command(name='set_channel', description='Set the channel where the bot listens for messages')
async def set_channel(ctx, channel: nextcord.TextChannel):
    if ctx.author.guild_permissions.administrator:
        save_channel_id(ctx.guild.id, channel.id)
        await ctx.send(f'Channel set to {channel.mention}!')
    else:
        await ctx.send('You must be an administrator to use this command.')

bot.run('YOUR_DISCORD_BOT_TOKEN')
