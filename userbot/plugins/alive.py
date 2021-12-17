import random
import re
import time
from datetime import datetime
from platform import python_version

from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, catub, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "Para verificar o status do bot",
        "options": "Para mostrar mídia neste cmd, você precisa definir ALIVE_PIC com link de mídia, obtenha isso respondendo à mídia por .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "Um negócio de mostrar detalhes do bot"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    catevent = await edit_or_reply(event, "`Checando...`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  ★ "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "**✮ `OLÁ MESTRE, O PAI TA ON` ✮**"
    CAT_IMG = gvarstatus("ALIVE_PIC")
    cat_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    caption = cat_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        catver=catversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if CAT_IMG:
        CAT = [x for x in CAT_IMG.split()]
        PIC = random.choice(CAT)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await catevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                catevent,
                f"**Erro de valor de mídia!!**\n__Altere o link por __`.setdv`\n\n**__Não é possível obter mídia deste link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            catevent,
            caption,
        )


temp = """{ALIVE_TEXT}
⟣⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⟢
👑 **Meu Dono :** {mention}
🐍 **Versão do Python :** v{pyver}
⚙️ **Versão do Telethon :** v{telever}
🐈 **Versão do Cat :** v{catver}
💻 **Funcionamento da Database :** {dbhealth}
⏰ **Tempo Ativo :** {uptime}
🏓 **Ping :** {ping}"""
