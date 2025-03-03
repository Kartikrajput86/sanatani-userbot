# Telegram Userbot

A simple Telegram userbot that runs on your user account.

## Setup Instructions

1. Get your API credentials:
   - Go to https://my.telegram.org
   - Login with your phone number
   - Click on 'API Development Tools'
   - Create a new application
   - Copy your API_ID and API_HASH

2. Set up the environment:
   - Copy `.env.example` to `.env`
   - Replace API_ID and API_HASH with your values

3. Install requirements:
   ```
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```
   python userbot.py
   ```

5. On first run, you'll need to enter your phone number and the verification code.

## Termux Setup Guide

1. Install required packages:
```bash
pkg update && pkg upgrade
pkg install python git
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/userbot
cd userbot
```

3. Install Python requirements:
```bash
pip install -r requirements.txt
```

4. Edit configuration:
- Open `bot.py`
- Update API_ID, API_HASH and BOT_TOKEN

5. Run the bot:
```bash
python bot.py
```

## Available Commands
- `.ping`: Bot will reply with "Pong!"

More commands can be added by modifying the userbot.py file.

## Features
- `.ping` - Check bot's ping
- `.alive` - Check bot's status
- `.raid` - Start raid
- `.draid` - Stop raid
- `.loveraid` - Start love raid
- `.dloveraid` - Stop love raid
- `.spam <count> <text>` - Spam messages
- `.help` - Show help message
- `.sudo` - Add sudo user
- `.sudolist` - List sudo users
- `.removesudo` - Remove sudo user
- `.mentionall` - Mention all users

## Clone Features
- `/clone <session>` - Clone a user account
- `/clonelist` - List all cloned users

## Owner
- [@innocenthr7](https://t.me/innocenthr7)

## Note
- All cloned users support same commands with . prefix
- Only main bot commands use / prefix
