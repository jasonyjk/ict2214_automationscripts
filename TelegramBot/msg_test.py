from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
import datetime
import subprocess

# Replace these with your own values
api_id = '24393142'
api_hash = 'ac5f008d615b5f15edc16c6d50dab3b8'
phone_number = '+6582881364'
bot_username = 'itp_msgbot'
message = '/start'

print("If you have to log in, type your phone number in international format +[Country Code][Phone Number].")
# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

def run_script(script_name):
    print("Reached RunScript function.")
    #python_executable = "C:/Users/buddy/AppData/Local/Microsoft/WindowsApps/python3.10.exe"
    #return subprocess.Popen([python_executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #return subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

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
    try:
        # Log in if required
        await client.start(phone_number)

        # Start sending continuous messages
        await send_continuous_messages()
    except FloodWaitError as e:
        print(e)
        await client.disconnect()
        run_script('automated_msg_2.py')
        return 1

with client:
    result = client.loop.run_until_complete(main())
    if result == 1:
        exit(1)