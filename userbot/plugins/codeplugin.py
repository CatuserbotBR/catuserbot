
import os
import re

import pygments
import requests
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from urlextract import URLExtract

from userbot import catub

from ..Config import Config
from ..core.events import MessageEdited
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import pastetext, reply_id

plugin_category = "utils"

extractor = URLExtract()

LOGS = logging.getLogger(__name__)

pastebins = {
    "Pasty": "p",
    "Neko": "n",
    "Spacebin": "s",
    "Dog": "d",
}


def get_key(val):
    for key, value in pastebins.items():
        if val == value:
            return key

@catub.cat_cmd(
    pattern="(d|p|s|n)?(pain|nekoin)(?:\s|$)([\S\s]*)",
    command=("pain", plugin_category),
    info={
        "header": "To paste text to a paste bin.",
        "description": "Uploads the given text to website so that you can share text/code with others easily. If no flag is used then it will use p as default",
        "flags": {
            "d": "Will paste text to dog.bin",
            "p": "Will paste text to pasty.lus.pm",
            "s": "Will paste text to spaceb.in (language extension not there at present.)",
        },
        "usage": [
            "{tr}{flags}pein <plugin name>",
        ],
        "examples": [
            "{tr}pain alive",
        ],
    },
)
async def why_odi_is_pro(zarox):
    "To paste plugin to a paste bin."
    input_str = zarox.pattern_match.group(3)
    if not input_str:
    	await edit_delete(zarox, "Are you comedy me")
    elif not os.path.exists(f"userbot/plugins/{input_str}.py"):
    	await edit_delete(zarox, "No such plugin installed in your userbot")
    else:
    	pass
    catevent = await edit_or_reply(zarox, "`Pasting plugin to paste bin....`")
    if zarox.pattern_match.group(2) == "nekoin":
        pastetype = "n"
    else:
        pastetype = zarox.pattern_match.group(1) or "p"
    plugin = f"userbot/plugins/{input_str}.py"
    with open(plugin, "r") as f:
        text = f.read()
    extension = ".py"
    try:
        response = await pastetext(text, pastetype, extension)
        if "error" in response:
            return await edit_delete(
                catevent,
                "**Error while pasting plugin:**\n`Unable to process your request may be pastebins are down.`",
            )

        result = f"<b>Pasted: {input_str}.py</b>"
        if pastebins[response["bin"]] != pastetype:
            result += f"<b>{get_key(pastetype)} is down, So </b>"
        result += f"\n<b>Pasted to: <a href={response['url']}>{response['bin']}</a></b>"
        if response["raw"] != "":
            result += f"\n<b>Raw link: <a href={response['raw']}>Raw</a></b>"
        await catevent.edit(result, link_preview=False, parse_mode="html")
    except Exception as e:
        await edit_delete(catevent, f"**Error while pasting plugin:**\n`{e}`")

@catub.cat_cmd(
    pattern="dango(?:\s|$)([\s\S]*)",
    command=("dango", plugin_category),
    info={
        "header": "Will paste the entire plugin on the blank white image.",
        "flags": {
            "f": "Use this flag to send it as file rather than image",
        },
        "usage": ["{tr}dango <reply>",],
    },
)
async def sadness(zarox):
    "To paste plugin to image."
    reply_to = await reply_id(zarox)
    input_str = zarox.pattern_match.group(1)
    ext = re.findall(r"-f", input_str)
    extension = None
    try:
        extension = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        extension = None
    if not input_str:
    	await edit_delete(zarox, "Are you comedy me")
    elif not os.path.exists(f"userbot/plugins/{input_str}.py"):
    	await edit_delete(zarox, "No such plugin installed in your userbot")
    else:
    	pass
    catevent = await edit_or_reply(zarox, "`Pasting the plugin on image`")
    plugin = f"userbot/plugins/{input_str}.py"
    with open(plugin, "r") as f:
        text_to_print = f.read()
    pygments.highlight(
        text_to_print,
        Python3Lexer(),
        ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
        "out.png",
    )
    try:
        await zarox.client.send_file(
            zarox.chat_id,
            "out.png",
            force_document=bool(extension),
            reply_to=reply_to,
        )
        await catevent.delete()
        os.remove("out.png")
        if d_file_name is not None:
            os.remove(d_file_name)
    except Exception as e:
        await edit_delete(catevent, f"**Error:**\n`{e}`", time=10)


