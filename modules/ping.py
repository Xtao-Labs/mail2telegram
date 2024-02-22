from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.incoming & filters.private & filters.command(["ping"]))
async def ping_command(_: Client, message: Message):
    await message.reply("pong~", quote=True)
