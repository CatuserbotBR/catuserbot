import asyncio
import requests
from time import time
from datetime import datetime

from . import hmention
from userbot import catub
from ..helpers.utils import reply_id
from ..helpers.functions import yt_search
from ..core.managers import edit_delete, edit_or_reply
from telethon.errors.rpcerrorlist import YouBlockedUserError

plugin_category = "misc"

def is_url(link):
    try:
        response = requests.get(link)
        url = "yes"
    except requests.exceptions.MissingSchema as exception:
        url = "no"
    return url

@catub.cat_cmd(
    pattern="(iyt)(a)?(?:\s|$)([\s\S]*)",
    command=("iyt", plugin_category),
    info={
        "header": "Para baixar vídeos/curtas ou áudio do youtube instantaneamente",
        "flags": {
            "a": "Para baixar em áudio."
        },
        "examples": [
            "{tr}iyt <inquerir/link/responder a um link>",
            "{tr}iyta <inquerir/link/responder a um link>",
        ],
        "notas": "Use .iyta para baixar áudio do yt e .iyt para baixar vídeo do yt",
    },
)
async def _(zarox):
    "For downloading yt video/shorts and audio instantly"
    chat = "@youtubednbot"
    reply_to_id = await reply_id(zarox)
    C = zarox.pattern_match.group(2)
    B = zarox.pattern_match.group(3)
    A = await zarox.get_reply_message()
    if A and A.message and not B:
        if "youtu" in A.message:
            mine = A.message
        else:
            return await edit_or_reply(zarox, "`Eu não consigo ler mentes, me dê algo para pesquisar`")
    elif B:
        yt_str = is_url(B)
        if yt_str == "yes" and "youtu" in B:
            mine = B
        else:
            mine = await yt_search(str(B))
    else:
        return await edit_or_reply(zarox, "`Eu não consigo ler mentes, dar algo para pesquisar`")
    await edit_or_reply(zarox, "**Baixando...**")
    async with zarox.client.conversation(chat) as conv:
        try:
            #await zarox.client(functions.account.UpdateNotifySettingsRequest(peer=chat, settings=types.InputPeerNotifySettings(show_previews=False, silent=True,)))
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                await zarox.client.send_read_acknowledge(conv.chat_id)
            except TimeoutError:
                return await edit_or_reply(zarox, "`Não foi possível baixar o vídeo. Tente mais tarde`")
            start = datetime.now()
            try:
                if C:
                    msg = await conv.send_message(f"/a {mine}", link_preview=True)
                else:
                    await asyncio.sleep(2)
                    msg = await conv.send_message(mine, link_preview=True)
                await asyncio.sleep(0.1)
                video = await conv.get_response()
            except TimeoutError:
                await zarox.client.delete_messages(conv.chat_id, [msg.id])
                if C:
                    msg = await conv.send_message(f"/a {mine}", link_preview=True)
                else:
                    await asyncio.sleep(2)
                    msg = await conv.send_message(mine, link_preview=True)
                await asyncio.sleep(0.1)
                video = await conv.get_response()
            await zarox.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await edit_or_reply(zarox, "**Erro:** `desbloqueie @youtubednbot `e tente novamente!`")
            return
        await zarox.delete()
        end = datetime.now()
        ms = (end - start).seconds
        caption = f"**➥ Link:** [link do vídeo]({mine})"
        cat = await zarox.client.send_file(
            zarox.chat_id,
            video,
            caption=caption,
            reply_to=reply_to_id,
        )
    await zarox.client.delete_messages(
        conv.chat_id, [msg_start.id, response.id, msg.id, video.id,]
    )
