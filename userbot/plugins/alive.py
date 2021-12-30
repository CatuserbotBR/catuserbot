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

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import StartTime, catub, catversion, mention

ANIME_QUOTE = [
    "Lembre-se da lição e não da decepção.",
    "Você não conhece as pessoas, você conhece apenas o que elas permitem que você veja.",
    "As vezes as questões são complicadas e as respostas são simples.",
    "Amar alguém profundamente lhe da força: ser amado profundamente lhe da coragem.",
    "Você não é derrotado quando perde, mas sim quando você desiste.",
    "Há momentos que você precisa desistir de alguma coisa para preservar a outra.",
    "A vida das pessoas não acaba quando elas morrem, mas sim quando perdem a fé‌.",
    "Se você está vivo pode recomeçar. Ninguém tem o direito de te tirar isso.",
    "O pessimismo, depois de você se acostumar com ele, é tão agradável quanto o otimismo.",
    "Perdoar é libertar o prisioneiro... e descobrir que o prisioneiro era você.",
    "Tudo o que um sonho precisa é alguém que acredite que ele possa ser realizado.",
    "Não espere por uma crise para descobrir o que é importante em sua vida.",
    "Descobrir consiste em olhar para o que o mundo está vendo e pensar uma coisa diferente.",
    "No fundo de um buraco ou de um poço, acontece a descoberta das estrelas.",
]
plugin_category = "utils"


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "Para o ver se o bot está ativo",
        "options": "Para mostrar mídia neste comando, você precisa definir ALIVE_PIC com link de mídia, obtenha isso respondendo à mídia por .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    ANIME = f"{random.choice(ANIME_QUOTE)}"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    catevent = await edit_or_reply(event, "`Checando...`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or ANIME
    CAT_IMG = gvarstatus("ALIVE_PIC")
    cat_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    caption = cat_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
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


temp = """`{ALIVE_TEXT}`

👑 **Meu Dono:** {mention}
🐍 **Versão do Python:** v{pyver}
⚙️ **Versão do Telethon:** v{telever}
🐈 **Versão do Cat**: v{catver}
💻 **Funcionamento da Database:** {dbhealth}
⏰ **Tempo Ativo:** {uptime}
🏓 **Ping:** {ping}ms"""
