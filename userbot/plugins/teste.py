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
    pattern="gap$",
    command=("gap", plugin_category),
    info={
        "header": "Repo do CatUserbot",
        "options": "Para mudar a img do use o .setdv IALIVEPIC link.",
        "usage": [
            "{tr}gap",
        ],
    },
)
async def amireallyalive(event):
    "oi"
    reply_to_id = await reply_id(event)
    

    cat_caption = "**Aqui estão os Gapps A11.**"
    
    
    
    
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, cat_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


