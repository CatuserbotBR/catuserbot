from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import catub, reply_id

plugin_category = "fun"

@catub.cat_cmd(
    pattern="xxshort ?(.*)",
    command=("xxshort", plugin_category),
    info={
        "header": "To download songs via DeezLoad bot",
        "description": "Spotify/Deezer downloader",
        "usage": "{tr}dzd <song link>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    chat = "@OpGufaBot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("🤪")
            response = await conv.get_response()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to_id)
        except YouBlockedUserError:
            await event.reply("```Unblock @OpGufaBot```")
            return


@catub.cat_cmd(
    pattern="xxlong ?(.*)",
    command=("xxlong", plugin_category),
    info={
        "header": "To download songs via DeezLoad bot",
        "description": "Spotify/Deezer downloader",
        "usage": "{tr}dzd <song link>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    await event.get_reply_message()
    chat = "@OpGufaBot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("😏")
            response = await conv.get_response()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to_id)
        except YouBlockedUserError:
            await event.reply("```Unblock @OpGufaBot```")
            return

@catub.cat_cmd(
    pattern="xpic ?(.*)",
    command=("xpic", plugin_category),
    info={
        "header": "To download songs via DeezLoad bot",
        "description": "Spotify/Deezer downloader",
        "usage": "{tr}dzd <song link>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    await event.get_reply_message()
    chat = "@OpGufaBot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("💋")
            response = await conv.get_response()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to_id)
        except YouBlockedUserError:
            await event.reply("```Unblock @OpGufaBot```")
            return

@catub.cat_cmd(
    pattern="xnxx ?(.*)",
    command=("xnxx", plugin_category),
    info={
        "header": "To download songs via DeezLoad bot",
        "description": "Spotify/Deezer downloader",
        "usage": "{tr}dzd <song link>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    chat = "@SeXn1bot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("💋2016 Videolar🔞")
            response = await conv.get_response()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to_id)
        except YouBlockedUserError:
            await event.reply("```Unblock @SeXn1bot```")
            return


@catub.cat_cmd(
    pattern="picx ?(.*)",
    command=("picx", plugin_category),
    info={
        "header": "To download songs via DeezLoad bot",
        "description": "Spotify/Deezer downloader",
        "usage": "{tr}dzd <song link>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    chat = "@SeXn1bot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("♨️Old photo👙")
            response = await conv.get_response()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to_id)
        except YouBlockedUserError:
            await event.reply("```Unblock @SeXn1bot```")
            return

@catub.cat_cmd(
    pattern="les (-s|$)",
    command=("les -s", plugin_category),
    info={
        "header": "To download songs via DeezLoad bot",
        "description": "Spotify/Deezer downloader",
        "usage": "{tr}dzd <song link>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    hm = event.pattern_match.group(1)
    chat = "@SeXn1bot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            if hm:
              await conv.send_message("🔞SeX_Vido🚷")
            else:  
              await conv.send_message("🔞Uz_sex♨️")
            response = await conv.get_response()
            await event.client.send_message(event.chat_id, response, reply_to=reply_to_id)
        except YouBlockedUserError:
            await event.reply("```Desbloqueie @SeXn1bot```")
            return
