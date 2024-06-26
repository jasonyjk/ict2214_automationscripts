import discord
import asyncio

TOKEN = 'MTI1NDc4Mzk2ODc5NzI2MTkwNA.GnD8q9.ZN3Hi0GI3StErYUpPSXrhD3mshceffzD4U8JwU'
CHANNEL_ID = 1234446166008270878

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected')
    channel = client.get_channel(CHANNEL_ID)
    await asyncio.sleep(2.5)
    while True:
        await channel.send('Hello from Bot 2!')
        await asyncio.sleep(5)  # Wait for 5 seconds before sending the next message

client.run(TOKEN)