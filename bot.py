from pyrogram import Client, filters
import asyncio
import random
from raid_messages import RAID_MESSAGES, LOVE_RAID_MESSAGES
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait, UserNotParticipant
import json
import os
import sys
from dotenv import load_dotenv   # <--- add this

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot configuration
app = Client(
    "sanatani_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

OWNER_USERNAME = os.getenv("OWNER_USERNAME", "teralover7")
OWNER_ID = int(os.getenv("OWNER_ID", "7653172279"))
active_raids = {}
active_clones = {}  # Store active clone sessions
sudo_users = set()
VERSION = "2.1.2"
SUDO_USERS_FILE = "sudo_users.json"

# Load sudo users from file
try:
    with open(SUDO_USERS_FILE, 'r') as f:
        sudo_users = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    sudo_users = set()
    with open(SUDO_USERS_FILE, 'w') as f:
        json.dump(list(sudo_users), f)

def save_sudo_users():
    with open(SUDO_USERS_FILE, 'w') as f:
        json.dump(list(sudo_users), f)

def is_sudo(user_id):
    return user_id in sudo_users or user_id == OWNER_ID

def get_uptime():
    uptime = int(time.time() - start_time)
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60
    return f"{hours}h {minutes}m {seconds}s"

HELP_MESSAGE = """
╭────── ˹ 𝛅ᴀɴᴀᴛᴀɴɪ ꭙ 𝐔sᴇꝛвσᴛ ˼ ⏤͟͟͞͞★
┆◍ ᴄᴏᴍᴍᴀɴᴅs:
┆• /ping - ᴄʜᴇᴄᴋ ʙᴏᴛ's ᴘɪɴɢ
┆• /alive - ᴄʜᴇᴄᴋ ʙᴏᴛ's sᴛᴀᴛᴜs
┆• /help - sʜᴏᴡ ᴛʜɪs ʜᴇʟᴘ
┆• /id, .id - ɢᴇᴛ ᴜsᴇʀ/ᴄʜᴀᴛ ɪᴅ
┆• /info, .info - ɢᴇᴛ ᴜsᴇʀ/ᴄʜᴀᴛ ɪɴғᴏ
┆• /raid - sᴛᴀʀᴛ ʀᴀɪᴅ
┆• /draid - sᴛᴏᴘ ʀᴀɪᴅ
┆• /loveraid - sᴛᴀʀᴛ ʟᴏᴠᴇ ʀᴀɪᴅ
┆• /dloveraid - sᴛᴏᴘ ʟᴏᴠᴇ ʀᴀɪᴅ
┆• /spam <count> <text> - sᴘᴀᴍ ᴍᴇssᴀɢᴇs
┆• /banall - ʙᴀɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs
┆• /broadcast - ʙʀᴏᴀᴄᴀsᴛ ᴍᴇssᴀɢᴇ
┆• /mentionall - ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs
╰─────────────────
"""

START_MESSAGE = """╭────── ˹ 𝛅ᴀɴᴀᴛᴀɴɪ ꭙ 𝐔sᴇꝛвσᴛ ˼ ⏤͟͟͞͞★
┆◍ ʜᴇʏ, ɪ ᴀᴍ : 𝛅ᴀɴᴀᴛᴀɴɪ ꭙ 𝐔sᴇꝛвσᴛ 
┆● 𝛅ᴀɴᴀᴛᴀɴɪ Bᴏᴛ Vᴇʀsɪᴏɴ : {version}
┊● Pᴏᴡᴇʀғᴜʟ & Usᴇғᴜʟ Usᴇʀʙᴏᴛ
┊● ᴄᴏᴍᴍᴀɴᴅs:
┊  • /help - sʜᴏᴡ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs
┊  • /ping - ᴄʜᴇᴄᴋ ʙᴏᴛ's ᴘɪɴɢ
┊  • /alive - ᴄʜᴇᴄᴋ ʙᴏᴛ's sᴛᴀᴛᴜs
┊  • /raid - sᴛᴀʀᴛ ʀᴀɪᴅ
┊  • /draid - sᴛᴏᴘ ʀᴀɪᴅ
┊  • /loveraid - sᴛᴀʀᴛ ʟᴏᴠᴇ ʀᴀɪᴅ
┊  • /dloveraid - sᴛᴏᴘ ʟᴏᴠᴇ ʀᴀɪᴅ
┊  • /spam - sᴘᴀᴍ ᴍᴇssᴀɢᴇs
┊  • /banall - ʙᴀɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs
┊  • /broadcast - ʙʀᴏᴀᴄᴀsᴛ ᴍᴇssᴀɢᴇ
┊  • /mentionall - ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs
┊● ᴄʟᴏɴᴇ ᴄᴏᴍᴍᴀɴᴅs:
┊  • /clone - ᴄʟᴏɴᴇ ᴀ ᴜsᴇʀ
╰─────────────────"""

@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ᴄʀᴇᴀᴛᴏʀ", url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/tibxfun")
        ],
        [
            InlineKeyboardButton("sᴇssɪᴏɴ ɢᴇɴ", url="https://t.me/PYsessionGenBot"),
            InlineKeyboardButton("ʜᴇʟᴘ", url="https://t.me/tibxowner")
        ]
    ])
    
    await message.reply_text(
        START_MESSAGE.format(version=VERSION),
        reply_markup=buttons
    )

@app.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text(HELP_MESSAGE)

@app.on_message(filters.command("ping"))
async def ping(client, message):
    start = time.time()
    reply = await message.reply_text("ᴘɪɴɢɪɴɢ...")
    end = time.time()
    await reply.edit_text(
        f"╭────── ˹ ᴘɪɴɢ ˼ ⏤͟͟͞͞★\n"
        f"┆◍ sᴘᴇᴇᴅ: {round((end - start) * 1000)}ᴍs\n"
        f"╰─────────────────"
    )

@app.on_message(filters.command("alive"))
async def alive(client, message):
    await message.reply_text(
        f"╭────── ˹ 𝛅ᴀɴᴀᴛᴀɴɪ ꭙ 𝐔sᴇꝛвσᴛ ˼ ⏤͟͟͞͞★\n"
        f"┆◍ sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ ✨\n"
        f"┆◍ ᴠᴇʀsɪᴏɴ: {VERSION}\n"
        f"┆◍ ᴜᴘᴛɪᴍᴇ: {get_uptime()}\n"
        f"┊◍ ᴏᴡɴᴇʀ: @{OWNER_USERNAME}\n"
        f"╰─────────────────"
    )

@app.on_message(filters.command("raid") & filters.user([OWNER_ID] + list(sudo_users)))
async def raid(client, message):
    chat_id = message.chat.id
    if chat_id not in active_raids:
        active_raids[chat_id] = True
        await message.reply_text("╭────── ˹ ʀᴀɪᴅ sᴛᴀʀᴛᴇᴅ ˼ ⏤͟͟͞͞★")
        while active_raids.get(chat_id):
            try:
                for _ in range(7):
                    await message.reply_text(random.choice(RAID_MESSAGES))
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Raid Error: {e}")
                break

@app.on_message(filters.command("draid") & filters.user([OWNER_ID] + list(sudo_users)))
async def draid(client, message):
    chat_id = message.chat.id
    if chat_id in active_raids:
        active_raids[chat_id] = False
        await message.reply_text("╭────── ˹ ʀᴀɪᴅ sᴛᴏᴘᴘᴇᴅ ˼ ⏤͟͟͞͞★")

@app.on_message(filters.command("loveraid") & filters.user([OWNER_ID] + list(sudo_users)))
async def loveraid(client, message):
    chat_id = message.chat.id
    if chat_id not in active_raids:
        active_raids[chat_id] = True
        await message.reply_text("╭────── ˹ ʟᴏᴠᴇ ʀᴀɪᴅ sᴛᴀʀᴛᴇᴅ ˼ ⏤͟͟͞͞★")
        while active_raids.get(chat_id):
            try:
                for _ in range(7):
                    await message.reply_text(random.choice(LOVE_RAID_MESSAGES))
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Love Raid Error: {e}")
                break

@app.on_message(filters.command("dloveraid") & filters.user([OWNER_ID] + list(sudo_users)))
async def dloveraid(client, message):
    chat_id = message.chat.id
    if chat_id in active_raids:
        active_raids[chat_id] = False
        await message.reply_text("╭────── ˹ ʟᴏᴠᴇ ʀᴀɪᴅ sᴛᴏᴘᴘᴇᴅ ˼ ⏤͟͟͞͞★")

@app.on_message(filters.command("spam") & filters.user([OWNER_ID] + list(sudo_users)))
async def spam(client, message):
    try:
        count = int(message.text.split()[1])
        text = " ".join(message.text.split()[2:])
        for _ in range(count):
            await message.reply_text(text)
            await asyncio.sleep(0.1)
    except (IndexError, ValueError):
        await message.reply_text("ᴜsᴇ: /spam <count> <text>")

@app.on_message(filters.command("broadcast") & filters.user([OWNER_ID] + list(sudo_users)))
async def broadcast(client, message):
    if not message.reply_to_message:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴄᴀsᴛ ɪᴛ")
        return
    
    success = 0
    failed = 0
    chat_list = []
    
    progress_msg = await message.reply_text("ʙʀᴏᴀᴄᴀsᴛɪɴɢ...")
    
    try:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in ["group", "supergroup", "channel"]:
                chat_list.append(dialog.chat.id)
    except Exception as e:
        await progress_msg.edit_text(f"Error getting dialogs: {str(e)}")
        return
    
    broadcast_msg = message.reply_to_message
    
    for chat_id in chat_list:
        try:
            await broadcast_msg.copy(chat_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await broadcast_msg.copy(chat_id)
            success += 1
        except Exception:
            failed += 1
        
        await progress_msg.edit_text(
            f"╭────── ˹ ʙʀᴏᴀᴄᴀsᴛɪɴɢ ˼ ⏤͟͟͞͞★\n"
            f"┆◍ ᴘʀᴏɢʀᴇss: {success + failed}/{len(chat_list)}\n"
            f"┆◍ sᴜᴄᴄᴇss: {success}\n"
            f"┆◍ ғᴀɪʟᴇᴅ: {failed}\n"
            f"╰─────────────────"
        )
        await asyncio.sleep(0.5)  # Avoid flood limits

@app.on_message(filters.command("clone"))
async def clone_user(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "╭────── ˹ 𝐂𝐋𝐎𝐍𝐄 𝐔𝐒𝐄𝐑 ˼ ⏤͟͟͞͞★\n"
                "┆◍ ᴜsᴀɢᴇ: /clone <session_string>\n"
                "┆◍ ᴄʟᴏɴᴇ ʏᴏᴜʀ ᴜsᴇʀʙᴏᴛ ᴀᴄᴄᴏᴜɴᴛ\n"
                "╰─────────────────"
            )
            return

        session_string = message.command[1]
        
        # Create new client session
        user = Client(
            f"user_{message.from_user.id}",
            api_id=20321413,
            api_hash="fd4966d99666af0f84d2e8efb445e270",
            session_string=session_string
        )
        
        try:
            await user.start()
            me = await user.get_me()
            
            # Store the client session
            active_clones[message.from_user.id] = {
                "client": user,
                "info": me,
                "session": session_string
            }
            
            # Add message handler for clone commands
            @user.on_message(filters.text & filters.me)
            async def handle_clone_commands(_, msg):
                if not msg.text.startswith('.'):
                    return
                    
                cmd = msg.text.split()[0].lower()
                if cmd == '.help':
                    await msg.edit_text("""╭────── ˹ 𝐂𝐋𝐎𝐍𝐄 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 ˼ ⏤͟͟͞͞★
┆◍ .ping - ᴄʜᴇᴄᴋ ᴘɪɴɢ
┆◍ .alive - ᴄʜᴇᴄᴋ sᴛᴀᴛᴜs
┆◍ .raid - sᴛᴀʀᴛ ʀᴀɪᴅ
┆◍ .draid - sᴛᴏᴘ ʀᴀɪᴅ
┆◍ .loveraid - sᴛᴀʀᴛ ʟᴏᴠᴇ ʀᴀɪᴅ
┆◍ .dloveraid - sᴛᴏᴘ ʟᴏᴠᴇ ʀᴀɪᴅ
┆◍ .spam <count> <text> - sᴘᴀᴍ ᴍᴇssᴀɢᴇs
┆◍ .banall - ʙᴀɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs
┆◍ .mentionall - ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ᴍᴇᴍʙᴇʀs
╰─────────────────""")
                elif cmd == '.ping':
                    start = time.time()
                    await msg.edit_text("ᴘɪɴɢɪɴɢ...")
                    end = time.time()
                    await msg.edit_text(f"╭────── ˹ ᴘɪɴɢ ˼ ⏤͟͟͞͞★\n┆◍ sᴘᴇᴇᴅ: {round((end - start) * 1000)}ᴍs\n╰─────────────────")
                elif cmd == '.alive':
                    await msg.edit_text(
                        f"╭────── ˹ 𝛅ᴀɴᴀᴛᴀɴɪ ꭙ 𝐔sᴇꝛвσᴛ ˼ ⏤͟͟͞͞★\n"
                        f"┆◍ sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ ✨\n"
                        f"┆◍ ᴠᴇʀsɪᴏɴ: {VERSION}\n"
                        f"┆◍ ᴜᴘᴛɪᴍᴇ: {get_uptime()}\n"
                        f"┆◍ ᴜsᴇʀ: {me.mention}\n"
                        f"╰─────────────────"
                    )
                elif cmd == '.raid':
                    active_raids[msg.chat.id] = True
                    await msg.edit_text("╭────── ˹ ʀᴀɪᴅ sᴛᴀʀᴛᴇᴅ ˼ ⏤͟͟͞͞★")
                    while active_raids.get(msg.chat.id):
                        try:
                            for _ in range(7):
                                await msg.reply_text(random.choice(RAID_MESSAGES))
                            await asyncio.sleep(1)
                        except Exception:
                            break
                elif cmd == '.draid':
                    if msg.chat.id in active_raids:
                        active_raids[msg.chat.id] = False
                        await msg.edit_text("╭────── ˹ ʀᴀɪᴅ sᴛᴏᴘᴘᴇᴅ ˼ ⏤͟͟͞͞★")
                elif cmd == '.loveraid':
                    active_raids[msg.chat.id] = True
                    await msg.edit_text("╭────── ˹ ʟᴏᴠᴇ ʀᴀɪᴅ sᴛᴀʀᴛᴇᴅ ˼ ⏤͟͟͞͞★")
                    while active_raids.get(msg.chat.id):
                        try:
                            for _ in range(7):
                                await msg.reply_text(random.choice(LOVE_RAID_MESSAGES))
                            await asyncio.sleep(1)
                        except Exception:
                            break
                elif cmd == '.dloveraid':
                    if msg.chat.id in active_raids:
                        active_raids[msg.chat.id] = False
                        await msg.edit_text("╭────── ˹ ʟᴏᴠᴇ ʀᴀɪᴅ sᴛᴏᴘᴘᴇᴅ ˼ ⏤͟͟͞͞★")
                elif cmd == '.spam':
                    if len(msg.text.split()) >= 3:
                        try:
                            count = int(msg.text.split()[1])
                            text = ' '.join(msg.text.split()[2:])
                            await msg.edit_text("╭────── ˹ sᴘᴀᴍᴍɪɴɢ ˼ ⏤͟͟͞͞★")
                            for _ in range(count):
                                await msg.reply_text(text)
                                await asyncio.sleep(0.1)
                        except ValueError:
                            await msg.edit_text("Invalid count!")
                    else:
                        await msg.edit_text("Usage: .spam <count> <text>")
                elif cmd == '.banall':
                    if msg.chat.type not in ['group', 'supergroup']:
                        await msg.edit_text("This command can only be used in groups!")
                        return
                        
                    # Check if user has ban rights
                    member = await msg.chat.get_member(me.id)
                    if not member.can_restrict_members:
                        await msg.edit_text("I don't have permission to ban members!")
                        return
                        
                    banned = 0
                    failed = 0
                    
                    await msg.edit_text("╭────── ˹ ʙᴀɴᴀʟʟ sᴛᴀʀᴛᴇᴅ ˼ ⏤͟͟͞͞★")
                    
                    async for member in user.get_chat_members(msg.chat.id):
                        if not member.user.is_bot:  # Skip bots
                            try:
                                await user.ban_chat_member(msg.chat.id, member.user.id)
                                banned += 1
                            except Exception:
                                failed += 1
                            
                            if (banned + failed) % 10 == 0:  # Update progress
                                await msg.edit_text(
                                    f"╭────── ˹ ʙᴀɴᴀʟʟ ˼ ⏤͟͟͞͞★\n"
                                    f"┆◍ ʙᴀɴɴᴇᴅ: {banned}\n"
                                    f"┆◍ ғᴀɪʟᴇᴅ: {failed}\n"
                                    f"╰─────────────────"
                                )
                            await asyncio.sleep(0.1)  # Avoid flood limits
                    
                    await msg.edit_text(
                        f"╭────── ˹ ʙᴀɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ˼ ⏤͟͟͞͞★\n"
                        f"┆◍ ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ: {banned}\n"
                        f"┆◍ ᴛᴏᴛᴀʟ ғᴀɪʟᴇᴅ: {failed}\n"
                        f"╰─────────────────"
                    )
                elif cmd == '.mentionall':
                    if msg.chat.type not in ['group', 'supergroup']:
                        await msg.edit_text("This command can only be used in groups!")
                        return
                        
                    mentioned = 0
                    failed = 0
                    text = ""
                    
                    await msg.edit_text("╭────── ˹ ᴍᴇɴᴛɪᴏɴɪɴɢ ᴀʟʟ ˼ ⏤͟͟͞͞★")
                    
                    async for member in user.get_chat_members(msg.chat.id):
                        try:
                            if not member.user.is_bot:  # Skip bots
                                text += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
                                mentioned += 1
                                
                                if len(text) > 3500:  # Telegram message limit is 4096
                                    await msg.reply_text(text)
                                    text = ""
                                    await asyncio.sleep(1)  # Avoid flood limits
                        except Exception:
                            failed += 1
                            
                        if mentioned % 50 == 0 and text:  # Send message every 50 mentions
                            await msg.reply_text(text)
                            text = ""
                            await asyncio.sleep(1)
                    
                    if text:  # Send any remaining mentions
                        await msg.reply_text(text)
                    
                    await msg.edit_text(
                        f"╭────── ˹ ᴍᴇɴᴛɪᴏɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ˼ ⏤͟͟͞͞★\n"
                        f"┆◍ ᴛᴏᴛᴀʟ ᴍᴇɴᴛɪᴏɴᴇᴅ: {mentioned}\n"
                        f"┆◍ ᴛᴏᴛᴀʟ ғᴀɪʟᴇᴅ: {failed}\n"
                        f"╰─────────────────"
                    )
                # ... rest of the clone commands ...
            
            await message.reply_text(
                f"╭────── ˹ 𝐂𝐋𝐎𝐍𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 ˼ ⏤͟͟͞͞★\n"
                f"┆◍ ᴜsᴇʀ: {me.first_name}\n"
                f"┆◍ ɪᴅ: {me.id}\n"
                f"┆◍ ᴜsᴇ .help ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs\n"
                f"╰─────────────────"
            )
            
        except Exception as e:
            await message.reply_text(f"Failed to start session: {str(e)}")
            if message.from_user.id in active_clones:
                await active_clones[message.from_user.id]["client"].stop()
                del active_clones[message.from_user.id]
            
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.command("mentionall"))
async def mention_all(client, message):
    try:
        if message.chat.type not in ['group', 'supergroup']:
            await message.reply_text("This command can only be used in groups!")
            return

        mentioned = 0
        failed = 0
        text = ""
        
        progress_msg = await message.reply_text("╭────── ˹ ᴍᴇɴᴛɪᴏɴɪɴɢ ᴀʟʟ ˼ ⏤͟͟͞͞★")
        
        async for member in client.get_chat_members(message.chat.id):
            try:
                if not member.user.is_bot:  # Skip bots
                    text += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
                    mentioned += 1
                    
                    if len(text) > 3500:  # Telegram message limit is 4096, we'll split at 3500 to be safe
                        await message.reply_text(text)
                        text = ""
                        await asyncio.sleep(1)  # Avoid flood limits
            except Exception:
                failed += 1
                
            if mentioned % 50 == 0 and text:  # Send message every 50 mentions
                await message.reply_text(text)
                text = ""
                await asyncio.sleep(1)
        
        if text:  # Send any remaining mentions
            await message.reply_text(text)
        
        await progress_msg.edit_text(
            f"╭────── ˹ ᴍᴇɴᴛɪᴏɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ˼ ⏤͟͟͞͞★\n"
            f"┆◍ ᴛᴏᴛᴀʟ ᴍᴇɴᴛɪᴏɴᴇᴅ: {mentioned}\n"
            f"┆◍ ᴛᴏᴛᴀʟ ғᴀɪʟᴇᴅ: {failed}\n"
            f"╰─────────────────"
        )
        
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.command("banall"))
async def ban_all(client, message):
    try:
        if message.chat.type not in ['group', 'supergroup']:
            await message.reply_text("This command can only be used in groups!")
            return
            
        # Check if bot has ban rights
        bot_member = await message.chat.get_member(client.me.id)
        if not bot_member.can_restrict_members:
            await message.reply_text("I don't have permission to ban members!")
            return

        banned = 0
        failed = 0
        
        progress_msg = await message.reply_text("╭────── ˹ ʙᴀɴᴀʟʟ sᴛᴀʀᴛᴇᴅ ˼ ⏤͟͟͞͞★")
        
        async for member in client.get_chat_members(message.chat.id):
            if member.user.id not in [OWNER_ID] + list(sudo_users):
                try:
                    await client.ban_chat_member(message.chat.id, member.user.id)
                    banned += 1
                except Exception:
                    failed += 1
                await asyncio.sleep(0.1)  # Avoid flood limits
                
                if (banned + failed) % 10 == 0:  # Update progress every 10 bans
                    await progress_msg.edit_text(
                        f"╭────── ˹ ʙᴀɴᴀʟʟ ˼ ⏤͟͟͞͞★\n"
                        f"┆◍ ʙᴀɴɴᴇᴅ: {banned}\n"
                        f"┆◍ ғᴀɪʟᴇᴅ: {failed}\n"
                        f"╰─────────────────"
                    )
        
        await progress_msg.edit_text(
            f"╭────── ˹ ʙᴀɴᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ˼ ⏤͟͟͞͞★\n"
            f"┆◍ ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ: {banned}\n"
            f"┆◍ ᴛᴏᴛᴀʟ ғᴀɪʟᴇᴅ: {failed}\n"
            f"╰─────────────────"
        )
        
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.command(["mentionall", "tagall"], prefixes=".") & filters.user([OWNER_ID] + list(sudo_users)))
async def mention_all(client, message: Message):
    chat_id = message.chat.id
    
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("❌ Reply to a message or provide text to mention with!")

    text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    if message.reply_to_message:
        text = message.reply_to_message.text or text

    async def get_chat_members(chat_id):
        members = []
        async for member in client.get_chat_members(chat_id):
            if not member.user.is_bot:
                members.append(member.user)
        return members

    try:
        mentions = []
        members = await get_chat_members(chat_id)
        for i in range(0, len(members), 5):
            chunk = members[i:i+5]
            mention_text = f"💫 {text}\n\n" + " ".join(f"[{m.first_name}](tg://user?id={m.id})" for m in chunk)
            mentions.append(mention_text)

        for mention in mentions:
            try:
                await client.send_message(chat_id, mention)
                await asyncio.sleep(0.5)  # Reduced delay for faster mentions
            except FloodWait as e:
                await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("sudo", prefixes=".") & filters.user(OWNER_ID))
async def add_sudo(client, message):
    if len(message.command) != 2:
        await message.reply_text("❌ Usage: .sudo <user_id>")
        return

    try:
        user_id = int(message.command[1])
        sudo_users.add(user_id)
        save_sudo_users()
        await message.reply_text(f"✨ Added {user_id} to sudo users!")
    except ValueError:
        await message.reply_text("❌ Please provide a valid user ID")

@app.on_message(filters.command("removesudo", prefixes=".") & filters.user(OWNER_ID))
async def remove_sudo(client, message):
    if len(message.command) != 2:
        await message.reply_text("❌ Usage: .removesudo <user_id>")
        return

    try:
        user_id = int(message.command[1])
        if user_id in sudo_users:
            sudo_users.remove(user_id)
            save_sudo_users()
            await message.reply_text(f"✨ Removed {user_id} from sudo users!")
        else:
            await message.reply_text("❌ User is not a sudo user")
    except ValueError:
        await message.reply_text("❌ Please provide a valid user ID")

@app.on_message(filters.command("sudolist", prefixes=".") & filters.user([OWNER_ID] + list(sudo_users)))
async def list_sudo(client, message):
    if not sudo_users:
        await message.reply_text("❌ No sudo users found!")
        return

    sudo_list = "✨ Sudo Users:\n\n"
    for user_id in sudo_users:
        try:
            user = await client.get_users(user_id)
            sudo_list += f"• {user.first_name} [`{user_id}`]\n"
        except:
            sudo_list += f"• Unknown User [`{user_id}`]\n"
    
    await message.reply_text(sudo_list)

@app.on_message(filters.command("spam", prefixes=".") & filters.user([OWNER_ID] + list(sudo_users)))
async def spam(client, message):
    if len(message.command) < 3:
        await message.reply_text("❌ Usage: .spam <count> <text>")
        return

    try:
        count = int(message.command[1])
        if count > 100:  # Limit spam count
            count = 100
        text = " ".join(message.command[2:])
        
        for _ in range(count):
            await message.reply_text(text)
            await asyncio.sleep(0.1)  # Reduced delay for faster spam
    except ValueError:
        await message.reply_text("❌ Please provide a valid number for count")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("restart") & filters.user([OWNER_ID] + list(sudo_users)))
async def restart(client, message):
    await message.reply_text("╭────── ˹ ʀᴇsᴛᴀʀᴛɪɴɢ... ˼ ⏤͟͟͞͞★")
    os.execv(sys.executable, [sys.executable] + sys.argv)

@app.on_message(filters.command(["id", "info"], prefixes=["/", "."]))
async def get_info(client, message):
    # Check if this is a clone session
    is_clone = client.name != "danatani_userbot"
    
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    chat = message.chat
    
    if user:
        user_info = f"╭────── ˹ ᴜsᴇʀ ɪɴғᴏ ˼ ⏤͟͟͞͞★\n┆◍ ᴜsᴇʀ ɪᴅ: `{user.id}`\n┆◍ ғɪʀsᴛ ɴᴀᴍᴇ: {user.first_name}\n"
        if user.last_name:
            user_info += f"┆◍ ʟᴀsᴛ ɴᴀᴍᴇ: {user.last_name}\n"
        if user.username:
            user_info += f"┆◍ ᴜsᴇʀɴᴀᴍᴇ: @{user.username}\n"
        user_info += f"┆◍ ᴍᴇɴᴛɪᴏɴ: {user.mention}\n"
        
    chat_info = f"┆◍ ᴄʜᴀᴛ ɪᴅ: `{chat.id}`\n┆◍ ᴄʜᴀᴛ ᴛʏᴘᴇ: {chat.type}\n"
    if chat.title:
        chat_info += f"┆◍ ᴄʜᴀᴛ ᴛɪᴛʟᴇ: {chat.title}\n"
    if chat.username:
        chat_info += f"┆◍ ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ: @{chat.username}\n"
    
    session_info = ""
    if is_clone:
        session_info = f"┆◍ sᴇssɪᴏɴ: ᴄʟᴏɴᴇ\n┆◍ ᴄʟᴏɴᴇ ɴᴀᴍᴇ: {client.name}\n"
    
    full_info = user_info + chat_info + session_info + "╰─────────────────"
    await message.reply_text(full_info)

import time
import asyncio
import os
from telethon import TelegramClient, events
from pyrogram import Client as PyroClient

# Pyrogram setup
app = PyroClient(
    "my_bot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# Telethon setup
telethon_client = TelegramClient("bot", int(os.getenv("API_ID")), os.getenv("API_HASH"))

async def main():
    print("Bot starting...")

    # Start Pyrogram aur Telethon ek sath
    await telethon_client.start(bot_token=os.getenv("BOT_TOKEN"))

    # Example: Telethon handler
    @telethon_client.on(events.NewMessage(pattern="/ping"))
    async def handler(event):
        await event.respond("Pong! ✅ (Telethon)")

# Run Pyrogram + Telethon together
await asyncio.gather(
    asyncio.Event().wait(),   # Pyrogram ko idle rakhne ka naya method
    telethon_client.run_until_disconnected()
)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())

