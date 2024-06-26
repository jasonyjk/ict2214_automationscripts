import discord
import asyncio

TOKEN = 'MTI1NDc2NTI3MzY5Nzc1MTEwNA.G60b5V.TiKlMNvWYt0mt7bJtEKGnOjh1qHXWbDPNdW-No'
CHANNEL_ID = 1234446166008270878

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