from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
import datetime

# Replace these with your own values
api_id = '25015690'
api_hash = 'f12dd5b83859d9140f7243f3fe19e46d'
phone_number = '+6580879563'
bot_username = 'itp_msgbot'
message = '/start'

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def send_continuous_messages():
    while True:
        # Find the bot
        bot = await client.get_entity(bot_username)

        # Send a message to the bot
        await client.send_message(bot, message)
        print(f"Message sent to {bot_username} at {datetime.datetime.now()}")

        # Wait for 10 seconds before sending the next message
        await asyncio.sleep(5)

async def main():
    await client.disconnect()
    try:
        # Log in if required
        await client.start(phone_number)

        # Start sending continuous messages
        await send_continuous_messages()
    except FloodWaitError as e:
        print(e)
        await client.log_out()
        await client.disconnect()
        return 1

with client:
    result = client.loop.run_until_complete(main())
    if result == 1:
        exit(1)