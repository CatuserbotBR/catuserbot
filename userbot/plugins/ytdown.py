import asyncio
from datetime import datetime

import requests
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.functions import yt_search
from ..helpers.utils import reply_id

plugin_category = "misc"


def is_url(link):
    try:
        requests.get(link)
        url = "yes"
    except requests.exceptions.MissingSchema as exception:
        url = "no"
    return url


@catub.cat_cmd(
    pattern="(iyt)(a)?(?:\s|$)([\s\S]*)",
    command=("iyt", plugin_category),
    info={
        "header": "Para baixar videos/shots do yt instantâneamente",
        "examples": [
            "{tr}iyt <pesquisa/link/responder a um link>",
            "{tr}iyta <pesquisa/link/responder a um link>",
        ],
    },
)
async def _(amintas):
    "For downloading yt video/shorts instantly"
    chat = "@youtubednbot"
    reply_to_id = await reply_id(amintas)
    C = amintas.pattern_match.group(2)
    B = amintas.pattern_match.group(3)
    A = await amintas.get_reply_message()
    if A and A.message and not B:
        if "youtu" in A.message:
            mine = A.message
        else:
            return await edit_or_reply(
                amintas, "`Não consigo ler mentes, me dê algo para pesquisar`"
            )
    elif B:
        yt_str = is_url(B)
        if yt_str == "yes" and "youtu" in B:
            mine = B
        else:
            mine = await yt_search(str(B))
    else:
        return await edit_or_reply(
            amintas, "`Não consigo ler mentes, me dê algo para pesquisar`"
        )
    await edit_or_reply(amintas, "**Baixando...**")
    async with amintas.client.conversation(chat) as conv:
        try:
            try:
                msg_start = await conv.send_message("/start")
                response = await conv.get_response()
                await amintas.client.send_read_acknowledge(conv.chat_id)
            except TimeoutError:
                return await edit_or_reply(
                    amintas, "`Não foi possível baixar o vídeo. Tente novamente.`"
                )
            start = datetime.now()
            try:
                if C:
                    msg = await conv.send_message(f"/a {mine}", link_preview=True)
                else:
                    msg = await conv.send_message(mine, link_preview=True)
                await asyncio.sleep(0.1)
                video = await conv.get_response()
            except TimeoutError:
                await amintas.client.delete_messages(conv.chat_id, [msg.id])
                if C:
                    msg = await conv.send_message(f"/a {mine}", link_preview=True)
                else:
                    msg = await conv.send_message(mine, link_preview=True)
                await asyncio.sleep(0.1)
                video = await conv.get_response()
            await amintas.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await edit_or_reply(
                amintas, "**Erro:** `desbloqueie` @youtubednbot `e tente novamente!`"
            )
            return
        await amintas.delete()
        end = datetime.now()
        (end - start).seconds
        try:
            caption = f"[{msg.media.webpage.title}]({mine})"
        except:
            caption = ""
        cat = await amintas.client.send_file(
            amintas.chat_id,
            video,
            caption=caption,
            reply_to=reply_to_id,
        )
    await amintas.client.delete_messages(
        conv.chat_id,
        [
            msg_start.id,
            response.id,
            msg.id,
            video.id,
        ],
    )
