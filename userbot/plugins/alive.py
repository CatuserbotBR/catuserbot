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
    "ʟᴇᴍʙʀᴇ-sᴇ ᴅᴀ ʟɪᴄ‌ᴀ‌ᴏ ᴇ ɴᴀ‌ᴏ ᴅᴀ ᴅᴇᴄᴇᴘᴄ‌ᴀ‌ᴏ.",
    "ᴠᴏᴄᴇ‌ ɴᴀ‌ᴏ ᴄᴏɴʜᴇᴄᴇ ᴀs ᴘᴇssᴏᴀs, ᴠᴏᴄᴇ‌ ᴄᴏɴʜᴇᴄᴇ ᴀᴘᴇɴᴀs ᴏ ǫᴜᴇ ᴇʟᴀs ᴘᴇʀᴍɪᴛᴇᴍ ǫᴜᴇ ᴠᴏᴄᴇ‌ ᴠᴇᴊᴀ.",
    "ᴀs ᴠᴇᴢᴇs ᴀs ǫᴜᴇsᴛᴏ‌ᴇs sᴀ‌ᴏ ᴄᴏᴍᴘʟɪᴄᴀᴅᴀs ᴇ ᴀs ʀᴇsᴘᴏsᴛᴀs sᴀ‌ᴏ sɪᴍᴘʟᴇs.",
    "ᴀᴍᴀʀ ᴀʟɢᴜᴇ‌ᴍ ᴘʀᴏꜰᴜɴᴅᴀᴍᴇɴᴛᴇ ʟʜᴇ ᴅᴀ‌ ꜰᴏʀᴄ‌ᴀ; sᴇʀ ᴀᴍᴀᴅᴏ ᴘʀᴏꜰᴜɴᴅᴀᴍᴇɴᴛᴇ ʟʜᴇ ᴅᴀ‌ ᴄᴏʀᴀɢᴇᴍ.",
    "ᴠᴏᴄᴇ‌ ɴᴀ‌ᴏ ᴇ‌ ᴅᴇʀʀᴏᴛᴀᴅᴏ ǫᴜᴀɴᴅᴏ ᴘᴇʀᴅᴇ, ᴍᴀs sɪᴍ ǫᴜᴀɴᴅᴏ ᴠᴏᴄᴇ‌ ᴅᴇsɪsᴛᴇ.",
    "ʜᴀ ᴍᴏᴍᴇɴᴛᴏs ǫᴜᴇ ᴠᴏᴄᴇ‌ ᴘʀᴇᴄɪsᴀ ᴅᴇsɪsᴛɪʀ ᴅᴇ ᴀʟɢᴜᴍᴀ ᴄᴏɪsᴀ ᴘᴀʀᴀ ᴘʀᴇsᴇʀᴠᴀʀ ᴀ ᴏᴜᴛʀᴀ.",
    "ᴀ ᴠɪᴅᴀ ᴅᴀs ᴘᴇssᴏᴀs ɴᴀ‌ᴏ ᴀᴄᴀʙᴀ ǫᴜᴀɴᴅᴏ ᴇʟᴀs ᴍᴏʀʀᴇᴍ, ᴍᴀs sɪᴍ ǫᴜᴀɴᴅᴏ ᴘᴇʀᴅᴇᴍ ᴀ ꜰᴇ‌.",
    "sᴇ ᴠᴏᴄᴇ‌ ᴇsᴛᴀ‌ ᴠɪᴠᴏ ᴘᴏᴅᴇ ʀᴇᴄᴏᴍᴇᴄ‌ᴀʀ. ɴɪɴɢᴜᴇ‌ᴍ ᴛᴇᴍ ᴏ ᴅɪʀᴇɪᴛᴏ ᴅᴇ ᴛᴇ ᴛɪʀᴀʀ ɪssᴏ.",
    "ᴏ ᴘᴇssɪᴍɪsᴍᴏ, ᴅᴇᴘᴏɪs ᴅᴇ ᴠᴏᴄᴇ‌ sᴇ ᴀᴄᴏsᴛᴜᴍᴀʀ ᴀ ᴇʟᴇ, ᴇ‌ ᴛᴀ‌ᴏ ᴀɢʀᴀᴅᴀ‌ᴠᴇʟ ǫᴜᴀɴᴛᴏ ᴏ ᴏᴛɪᴍɪsᴍᴏ.",
    "ᴘᴇʀᴅᴏᴀʀ ᴇ‌ ʟɪʙᴇʀᴛᴀʀ ᴏ ᴘʀɪsɪᴏɴᴇɪʀᴏ... ᴇ ᴅᴇsᴄᴏʙʀɪʀ ǫᴜᴇ ᴏ ᴘʀɪsɪᴏɴᴇɪʀᴏ ᴇʀᴀ ᴠᴏᴄᴇ‌.",
    "ᴛᴜᴅᴏ ᴏ ǫᴜᴇ ᴜᴍ sᴏɴʜᴏ ᴘʀᴇᴄɪsᴀ ᴇ‌ ᴀʟɢᴜᴇ‌ᴍ ǫᴜᴇ ᴀᴄʀᴇᴅɪᴛᴇ ǫᴜᴇ ᴇʟᴇ ᴘᴏssᴀ sᴇʀ ʀᴇᴀʟɪᴢᴀᴅᴏ.",
    "ɴᴀ‌ᴏ ᴇsᴘᴇʀᴇ ᴘᴏʀ ᴜᴍᴀ ᴄʀɪsᴇ ᴘᴀʀᴀ ᴅᴇsᴄᴏʙʀɪʀ ᴏ ǫᴜᴇ ᴇ‌ ɪᴍᴘᴏʀᴛᴀɴᴛᴇ ᴇᴍ sᴜᴀ ᴠɪᴅᴀ.",
    "ᴏ ᴘᴇssɪᴍɪsᴍᴏ, ᴅᴇᴘᴏɪs ᴅᴇ ᴠᴏᴄᴇ‌ sᴇ ᴀᴄᴏsᴛᴜᴍᴀʀ ᴀ ᴇʟᴇ, ᴇ‌ ᴛᴀ‌ᴏ ᴀɢʀᴀᴅᴀ‌ᴠᴇʟ ǫᴜᴀɴᴛᴏ ᴏ ᴏᴛɪᴍɪsᴍᴏ.",
    "ᴅᴇsᴄᴏʙʀɪʀ ᴄᴏɴsɪsᴛᴇ ᴇᴍ ᴏʟʜᴀʀ ᴘᴀʀᴀ ᴏ ǫᴜᴇ ᴛᴏᴅᴏ ᴍᴜɴᴅᴏ ᴇsᴛᴀ‌ ᴠᴇɴᴅᴏ ᴇ ᴘᴇɴsᴀʀ ᴜᴍᴀ ᴄᴏɪsᴀ ᴅɪꜰᴇʀᴇɴᴛᴇ.",
    "ɴᴏ ꜰᴜɴᴅᴏ ᴅᴇ ᴜᴍ ʙᴜʀᴀᴄᴏ ᴏᴜ ᴅᴇ ᴜᴍ ᴘᴏᴄ‌ᴏ, ᴀᴄᴏɴᴛᴇᴄᴇ ᴅᴇsᴄᴏʙʀɪʀ-sᴇ ᴀs ᴇsᴛʀᴇʟᴀs.",
]
plugin_category = "utils"


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
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
                f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            catevent,
            caption,
        )


temp = """{ALIVE_TEXT}

👑 **Meu Dono:** {mention}
🐍 **Versão do Python:** v{pyver}
⚙️ **Versão do Telethon:** v{telever}
🐈 **Versão do Cat**: v{catver}
💻 **Funcionamento da Database:** {dbhealth}
⏰ **Tempo Ativo:** {uptime}
🏓 **Ping:** {ping}ms"""
