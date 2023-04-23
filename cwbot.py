import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
#intents.auto_moderation = True
#intents.moderation = True
#intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store the last message sent by each user
last_messages = {}

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    user_id = message.author.id
    print('message detected')

    # Check if the message contains attachments
    print(message)
    if len(message.attachments) > 0:
        print('has attachments')
        content_warning = False

        # Check if the last message sent by the user was a content warning
        if user_id in last_messages:
            content_warning = last_messages[user_id].content.lower().startswith("content warning") or last_messages[user_id].content.lower().startswith("cw:")

        for attachment in message.attachments:
            # Check if the attachment is marked as a spoiler and if the last message was a content warning
            if not attachment.is_spoiler() and not content_warning:
                print('Unspoled image detected!')
                # Delete the message
                # Send a warning to the user
                warning_message = f"{message.author.mention}, please add a spoiler to your media message and write a content warning before sending spoiler-covered media. Write 'Content warning' or 'CW:' in the start of the message"
                await message.channel.send(warning_message)
                await message.delete()
                return

    # Update the last message sent by the user
    last_messages[user_id] = message

    # Process commands if any
    await bot.process_commands(message)

bot.run('')# PUT YOUR BOT ID HERE
