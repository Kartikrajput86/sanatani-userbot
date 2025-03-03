from telethon import TelegramClient, events
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API credentials from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

# Create the client
client = TelegramClient('user_session', API_ID, API_HASH)

# Message handler
@client.on(events.NewMessage(pattern='.ping'))
async def ping_handler(event):
    await event.reply('Pong!')

# Start the client
if __name__ == '__main__':
    print("Starting userbot...")
    client.start()
    print("Userbot is running!")
    client.run_until_disconnected()
