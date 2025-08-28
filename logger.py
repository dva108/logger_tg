from telethon import TelegramClient, events
from datetime import datetime
import os

api_id = 12345678
api_hash = '0123456789qwerty9876543210qwerty'
channel_id = -1001234567890

client = TelegramClient('logger', api_id, api_hash)

@client.on(events.NewMessage(outgoing=True))
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_id = event.chat_id
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")

        if hasattr(chat, 'title'):
            chat_name = chat.title
            if str(chat_id).startswith("-100"):
                link_id = str(chat_id)[4:]
                chat_link = f"<a href='https://t.me/c/{link_id}'>{chat_name}</a>"
            else:
                chat_link = chat_name
        elif hasattr(chat, 'username') and chat.username:
            chat_name = f"{chat.first_name} @{chat.username}"
            chat_link = f"<a href='https://t.me/{chat.username}'>{chat_name}</a>"
        else:
            chat_name = chat.first_name or "Unknown"
            chat_link = chat_name

        header = f"{chat_link}   {timestamp}"

        if event.message.media:
            caption = f"{header}"
            if event.message.message:
                caption += f"\n\n{event.message.message}"

            await client.send_file(
                channel_id,
                file=event.message.media,
                caption=caption,
                parse_mode='html',
                force_document=False,
                link_preview=False
            )
        elif event.message.message:
            await client.send_message(
                channel_id,
                f"{header}\n\n{event.message.message}",
                parse_mode='html',
                link_preview=False
            )
    except Exception as e:
        # log error
        print(f"Error in new_message_handler: {e}")


client.start()
print("Logger started.")
client.run_until_disconnected()
