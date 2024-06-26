import discord
import asyncio

# Insert Discord bot token and channel ID here.
TOKEN = 'BOT TOKEN HERE'
CHANNEL_ID = 'CHANNEL ID HERE'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():

    #Bot connection to Discord established.
    print(f'{client.user} has connected')

    # Find discord channel ID
    channel = client.get_channel(CHANNEL_ID)

    # Send messages every 5 seconds, after a 2.5 second sleep. This will make sure that this bot
    # and the first bot will alternate messaging instead of sending together.
    await asyncio.sleep(2.5)
    while True:
        await channel.send('Hello from Bot 2!')
        await asyncio.sleep(5)  # Wait for 5 seconds before sending the next message

client.run(TOKEN)