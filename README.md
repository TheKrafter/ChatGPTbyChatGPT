# ChatGPT Discord Bot

ChatGPT is a simple Discord bot powered by OpenAI's GPT-3 language model. It listens to messages in a specified channel and generates a response based on the input using natural language processing. This bot is built using Python and the nextcord and openai libraries.
## Features

 * Generate responses using OpenAI's GPT-3 language model
 * Listen to messages in a specific channel in a Discord server
 * Set the channel where the bot listens for messages using a slash command
 * Save and fetch the channel ID to and from a YAML file
 * Customizable response length and temperature

## Usage

 1. Clone this repository and navigate to the project directory.

 2. Install the required Python libraries by running pip install -r requirements.txt.

 3. Create a new Discord bot and obtain its API token.

 4. Obtain an API key for OpenAI's GPT-3 language model.

 5. Create a config.yml file and fill in the following values:

     ```yaml

     OPENAI_API_KEY: <your_openai_api_key>
     DISCORD_BOT_TOKEN: <your_discord_bot_token>
     ```

 6. Run the bot by running python bot.py.

 7. Invite the bot to your Discord server by generating an invite link using the Discord Developer Portal.

 8. Use the /set_channel slash command to set the channel where the bot listens for messages:

     ```bash

      /set_channel #my-channel
     ```

     Replace #my-channel with the name of the channel you want to use.

 9. Start chatting with the bot! The bot will respond to any message sent in the specified channel.

## Credits

This bot was created by [Your Name Here]. Feel free to use and modify this code for your own purposes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Disclaimer
This project is mostly written by OpenAI's ChatGPT (except for the text under this header). Whether it works or not is not my problem.
