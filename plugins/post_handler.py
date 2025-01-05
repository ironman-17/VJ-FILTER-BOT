import re
from pyrogram.types import Message

async def handle_post_command(client, message: Message, user_states: dict):
    """
    Handles the /post command. Initializes the user state for adding files.
    """
    try:
        await message.reply(
            "**Welcome to the Rare Movie Post Feature!**\n\n"
            "**👉 Send the number of files you want to add 👈**\n\n"
            "**‼️ Note: Only numbers are allowed.**",
            disable_web_page_preview=True
        )
        user_states[message.chat.id] = {"state": "awaiting_num_files"}
    except Exception as e:
        await message.reply(f"Error occurred: {e}")

async def handle_message(client, message: Message, user_states: dict, direct_gen_db: int, temp, imdb_info, short_link):
    """
    Handles user messages based on their current state.
    """
    try:
        chat_id = message.chat.id

        if chat_id in user_states:
            current_state = user_states[chat_id]["state"]

            if current_state == "awaiting_num_files":
                await handle_num_files_state(message, user_states)

            elif current_state == "awaiting_files":
                await handle_files_state(client, message, user_states, direct_gen_db, temp, short_link)

            elif current_state == "awaiting_title":
                await handle_title_state(message, user_states, imdb_info, short_link)

        else:
            return
    except Exception as e:
        await message.reply(f"Error occurred: {e}")

async def handle_num_files_state(message: Message, user_states: dict):
    """
    Handles the 'awaiting_num_files' state where the user specifies the number of files.
    """
    try:
        num_files = int(message.text.strip())
        if num_files <= 0:
            await message.reply("Invalid input. Please enter a number greater than 0.")
            return

        user_states[message.chat.id] = {
            "state": "awaiting_files",
            "num_files": num_files,
            "files_received": 0,
            "file_ids": [],
            "file_sizes": [],
            "stream_links": []
        }

        await message.reply("**⏩ Forward the first file.**")
    except ValueError:
        await message.reply("Invalid input. Please enter a valid number.")

async def handle_files_state(client, message: Message, user_states: dict, direct_gen_db: int, temp, short_link):
    """
    Handles the 'awaiting_files' state where the user forwards the files.
    """
    chat_id = message.chat.id
    user_data = user_states[chat_id]

    if message.media:
        forwarded_message = await message.copy(chat_id=direct_gen_db)
        file_id = forwarded_message.message_id
        file_size = getattr(message, message.media.value).file_size
        stream_link = await short_link(f"https://t.me/{temp.U_NAME}?start=aNsH_{file_id}")

        user_data["file_ids"].append(file_id)
        user_data["file_sizes"].append(file_size)
        user_data["stream_links"].append(stream_link)

        user_data["files_received"] += 1
        files_received = user_data["files_received"]
        num_files_left = user_data["num_files"] - files_received

        if num_files_left > 0:
            await message.reply(f"**⏩ Forward file no. {files_received + 1}.**")
        else:
            await message.reply("**Now send the movie title or name.**")
            user_data["state"] = "awaiting_title"
    else:
        await message.reply("No media detected. Please forward a valid file.")

async def handle_title_state(message: Message, user_states: dict, imdb_info, short_link):
    """
    Handles the 'awaiting_title' state where the user sends the movie title.
    """
    chat_id = message.chat.id
    title = message.text.strip()
    cleaned_title = re.sub(r"[()\[\]{}:;'!]", "", title)

    poster_url = imdb_info.get("poster") if imdb_info else "https://telegra.ph/file/74707bb075903640ed3f6.jpg"

    user_data = user_states[chat_id]
    file_info = "\n\n".join([
        f"》{size} : {await short_link(link)}"
        for size, link in zip(user_data["file_sizes"], user_data["stream_links"])
    ])

    summary_message = (
        f"**🎬 {cleaned_title}**\n\n"
        "**[360p☆480p☆Hevc☆720p☆1080p]**\n\n"
        "**Direct Telegram Files Only:**\n\n"
        f"{file_info}\n\n"
        "**✅ Note: [How to Download](https://example.com)**\n\n"
        "**⚡ Join: @Movieprovidergroups**"
    )

    await message.reply_photo(poster_url, caption=summary_message)
    del user_states[chat_id]
    
