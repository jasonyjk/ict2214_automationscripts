import discord
import asyncio

TOKEN = 'BOT TOKEN HERE'
CHANNEL_ID = 'CHANNEL ID HERE'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected')
    channel = client.get_channel(CHANNEL_ID)
    while True:
        await channel.send('Hello from Bot 1!')
        await asyncio.sleep(5)  # Wait for 5 seconds before sending the next message

client.run(TOKEN)