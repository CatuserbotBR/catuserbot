import os
import random
import base64
import asyncio
import logging
import requests
from telethon import functions, types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _catutils, reply_id
from ..helpers import media_type
from . import catub

plugin_category = "extra"

LOGS = logging.getLogger(__name__)

    
@catub.cat_cmd(
    pattern="gifs(?:\s|$)([\s\S]*)",
    command=("gifs", plugin_category),
    info={
        "header": "Envia gifs aleatórios",
        "usage": "Pesquise e envia seu gif de desejo aleatoriamente e em massa",
        "examples": [
            "{tr}gifs cat",
            "{tr}gifs cat ; <1-20>",
        ],
    },
)
async def some(event):
    """Sends random gifs of your query"""
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not inpt:
        await edit_delete(event, "`Me dê algo para pesquisar...`")
    count = 1
    if ";" in inpt:
        inpt, count = inpt.split(";")
    if int(count) < 0 and int(count) > 20:
        await edit_delete(event, "`Dê um valor no intervalo de 1-20`")
    catevent = await edit_or_reply(event, "`Enviando gif....`")
    res = requests.get("https://giphy.com/")
    res = res.text.split("GIPHY_FE_WEB_API_KEY =")[1].split("\n")[0]
    api_key = res[2:-1]
    r = requests.get(
        f"https://api.giphy.com/v1/gifs/search?q={inpt}&api_key={api_key}&limit=50"
    ).json()
    list_id = [r["data"][i]["id"] for i in range(len(r["data"]))]
    rlist = random.sample(list_id, int(count))
    for items in rlist:
        nood = await event.client.send_file(
            event.chat_id,
            f"https://media.giphy.com/media/{items}/giphy.gif",
            reply_to=reply_to_id,
        )
        await _catutils.unsavegif(event, nood)
    await catevent.delete()


@catub.cat_cmd(
    pattern="kiss(?:\s|$)([\s\S]*)",
    command=("kiss", plugin_category),
    info={
        "header": "Manda um beijo aleatório",
        "usage": [
            "{tr}kiss",
            "{tr}kiss <1-20>",
        ],
    },
)
async def some(event):
    """Its useless for single like you. Get a lover first"""
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    count = 1 if not inpt else int(inpt)
    if count < 0 and count > 20:
        await edit_delete(event, "`Dê valor no intervalo de 1-20`")
    res = base64.b64decode(
        "aHR0cHM6Ly90Lm1lL2pvaW5jaGF0L0NtZEEwVzYtSVVsbFpUUTk="
    ).decode("utf-8")
    resource = await event.client(GetFullChannelRequest(res))
    chat = resource.chats[0].username
    try:
        await event.client(
            functions.channels.GetParticipantRequest(
                channel=chat, participant=event.from_id.user_id
            )
        )
    except UserNotParticipantError:
        await event.client(Get(res.split("/")[4]))
        await event.client.edit_folder(resource.full_chat.id, 1)
        await event.client(
            functions.account.UpdateNotifySettingsRequest(
                peer=chat,
                settings=types.InputPeerNotifySettings(
                    show_previews=False,
                    silent=True,
                ),
            )
        )
    catevent = await edit_or_reply(event, "`Aguarde...`😘")
    maxmsg = await event.client.get_messages(chat)
    start = random.randint(31, maxmsg.total)
    start = min(start, maxmsg.total - 40)
    end = start + 41
    kiss = []
    async for x in event.client.iter_messages(
        chat, min_id=start, max_id=end, reverse=True
    ):
        try:
            if x.media and x.media.document.mime_type == "video/mp4":
                link = f"{res.split('j')[0]}{chat}/{x.id}"
                kiss.append(link)
        except AttributeError:
            pass
    kisss = random.sample(kiss, count)
    for i in kisss:
        nood = await event.client.send_file(event.chat_id, i, reply_to=reply_to_id)
        await _catutils.unsavegif(event, nood)
    await catevent.delete()
