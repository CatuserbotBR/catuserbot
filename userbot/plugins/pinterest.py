#Created by @MineisZarox t.me/IrisZarox

import os
import re
import requests
import asyncio
from userbot import catub
from . import mention
from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id
from urllib import request
try:
    from pyquery import PyQuery as pq
except ModuleNotFoundError:
    os.system("pip3 install pyquery")
    from pyquery import PyQuery as pq

plugin_category = "extra"

def get_download_url(link):
    post_request = requests.post('https://www.expertsphp.com/download.php', data={'url': link})

    request_content = post_request.content
    str_request_content = str(request_content, 'utf-8')
    download_url = pq(str_request_content)('table.table-condensed')('tbody')('td')('a').attr('href')
    return download_url


@catub.cat_cmd(
    pattern="pint(?:\s|$)([\s\S]*)",
    command=("pint", plugin_category),
    info={
        "header": "Para baixar postagens do pinterest",
        "options": "Para baixar postagens de imagem e vídeo do pinterest",
        "usage": [
            "{tr}pint <link do post>",
        ],
    },
)

async def pint(event):
    "To download pinterest posts"
    A = event.pattern_match.group(1)
    B = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    if A:
        MINE = get_download_url(A)
    elif B and B.message:
    	MINE = get_download_url(B.message)
    else:
        return await edit_delete(event, "`Forneça um link junto com cmd ou responda a um link`")
    if A and "pint" not in A:
        await edit_or_reply(event, "`Por favor, dê um link pinterest válido`")
        return
    elif not A and "pint" not in B.message:
        await edit_or_reply(event, "`Por favor, dê um link pinterest válido`")
        return
    else:
    	pass
    await edit_or_reply(event, "`Baixando...`")
    await event.delete()
    await event.client.send_file(event.chat.id, MINE, caption=f"➥Enviado por = {mention}", reply_to=reply_to_id)
    
    
