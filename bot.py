# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

import plugins.post_handler
from pyrogram import Client, idle
from database.users_chats_db import db
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server
from plugins.clone import restart_bots

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)
TechVJBot.start()
loop = asyncio.get_event_loop()


async def start():
    print('\n')
    print('Initalizing Your Bot')
    bot_info = await TechVJBot.get_me()
    await initialize_clients()
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Tech VJ Imported => " + plugin_name)
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    try:
        await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except:
        print("Make Your Bot Admin In Log Channel With Full Rights")
    for ch in CHANNELS:
        try:
            k = TechVJBot.send_message(chat_id=ch, text="**Bot Restarted**")
            await k.delete()
        except:
            print("Make Your Bot Admin In File Channels With Full Rights")
    try:
        k = await TechVJBot.send_message(chat_id=AUTH_CHANNEL, text="**Bot Restarted**")
        await k.delete()
    except:
        print("Make Your Bot Admin In Force Subscribe Channel With Full Rights")
    if CLONE_MODE == True:
        print("Restarting All Clone Bots.......")
        await restart_bots()
        print("Restarted All Clone Bots.")
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    await idle()


if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')

from pyrogram import Client, filters  # Required imports
import re  # For text processing

# Global variables
user_states = {}  # Manage user states during interaction
DIRECT_GEN_DB = -100123456789  # Replace with your target channel/group ID
ADMINS = [123456789, 987654321]  # Replace with Telegram user IDs of admins

# Utility function: Clean title
def clean_title(title):
    return re.sub(r"\s+", " ", title).strip()

# Main function: Handle `/post` command
@Client.on_message(filters.command("post") & filters.user(ADMINS))
async def post_command(client, message):
    try:
        await message.reply(
            "**Wᴇʟᴄᴏᴍᴇ Tᴏ Usᴇ Oᴜʀ Rᴀʀᴇ Mᴏᴠɪᴇ Pᴏsᴛ Fᴇᴀᴛᴜʀᴇ :)**\n\n"
            "**👉🏻 Sᴇɴᴅ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ғɪʟᴇs ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴀᴅᴅ 👈🏻**\n\n"
            "**‼️ Nᴏᴛᴇ: Oɴʟʏ ɴᴜᴍʙᴇʀs ᴀʟʟᴏᴡᴇᴅ**",
            disable_web_page_preview=True,
        )
        user_states[message.chat.id] = {"state": "awaiting_num_files"}
    except Exception as e:
        await message.reply(f"Error occurred: {e}")

# Function: Handle file uploads and title input
@Client.on_message(filters.private & (filters.text | filters.media) & ~filters.command("post"))
async def handle_message(client, message):
    try:
        chat_id = message.chat.id

        # Check if user is in a session
        if chat_id in user_states:
            current_state = user_states[chat_id]["state"]

            # Step 1: Expect number of files
            if current_state == "awaiting_num_files":
                try:
                    num_files = int(message.text.strip())

                    if num_files <= 0:
                        await message.reply("⏩ Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴘᴏsɪᴛɪᴠᴇ ɴᴜᴍʙᴇʀ.")
                        return

                    user_states[chat_id] = {
                        "state": "awaiting_files",
                        "num_files": num_files,
                        "files_received": 0,
                        "file_ids": [],
                        "file_sizes": [],
                    }

                    await message.reply("**⏩ Fᴏʀᴡᴀʀᴅ Tʜᴇ ғɪʀsᴛ ғɪʟᴇ**")
                except ValueError:
                    await message.reply("**Invalid input. Please send a valid number.**")

            # Step 2: Expect file uploads
            elif current_state == "awaiting_files":
                if not message.media:
                    await message.reply("⏩ Pʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴀ ғɪʟᴇ.")
                    return

                file_id = message.message_id  # Store file message ID
                user_states[chat_id]["file_ids"].append(file_id)
                user_states[chat_id]["files_received"] += 1

                files_left = (
                    user_states[chat_id]["num_files"] - user_states[chat_id]["files_received"]
                )

                if files_left > 0:
                    await message.reply(f"**⏩ Fᴏʀᴡᴀʀᴅ Tʜᴇ ɴᴇxᴛ ғɪʟᴇ (ᴛᴏᴛᴀʟ: {files_left})**")
                else:
                    await message.reply("**Nᴏᴡ, sᴇɴᴅ ᴛʜᴇ ᴍᴏᴠɪᴇ Tɪᴛʟᴇ ᴏʀ Nᴀᴍᴇ.**")
                    user_states[chat_id]["state"] = "awaiting_title"

            # Step 3: Expect title
            elif current_state == "awaiting_title":
                title = message.text.strip()
                title_clean = clean_title(title)

                # Generate file info
                file_info = "\n\n".join(
                    [f"》File ID: {file_id}" for file_id in user_states[chat_id]["file_ids"]]
                )

                summary = (
                    f"**🎬 {title_clean}**\n\n"
                    f"**📂 Files Uploaded:**\n\n{file_info}\n\n"
                    "**⚡ Thank you for using the bot!**"
                )

                await message.reply(summary)
                del user_states[chat_id]  # Clear user session

    except Exception as e:
        await message.reply(f"Error occurred: {e}")
        
