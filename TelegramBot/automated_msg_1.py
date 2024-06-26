from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
import datetime

# Replace these with your own values
api_id = 'API ID HERE'
api_hash = 'API HASH HERE'
phone_number = '+65[PHONE NUMBER HERE]'
bot_username = 'BOT USERNAME HERE'
message = '/start'

print("If you have to log in, type your phone number in international format +[Country Code][Phone Number].")
# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

# Function to send continuous messages FROM YOUR OWN TELEGRAM ACCOUNT.
async def send_continuous_messages():
    while True:
        # Find the bot
        bot = await client.get_entity(bot_username)

        # Send a message to the bot
        await client.send_message(bot, message)
        print(f"Message sent to {bot_username} at {datetime.datetime.now()}")

        # Wait for 5 seconds before sending the next message

        # This value can be modified to edit the interval, but for a rough calculation, take the value here and multiply it by 2 to get 
        # the rough amount of minutes that the script will run for before hitting an API block (FloodWaitError).
        #
        #  In this current set of code, it's about 10 minutes.
        await asyncio.sleep(5)

async def main():
    try:
        # Start sending continuous messages
        await send_continuous_messages()

    # Eventually around 10 minutes, there will be a Telegram API block. 
    # This section detects that block and logs you out automatically.
    except FloodWaitError as e:
        print(e)
        await client.log_out()
        await client.disconnect()
        return 1

# Set continuous loop to run main.       
with client:
    result = client.loop.run_until_complete(main())
    if result == 1:
        exit(1)