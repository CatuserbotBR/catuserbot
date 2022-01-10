import os

from PIL import Image, ImageEnhance

from userbot import catub

from ..core.managers import edit_delete
from ..helpers.utils import reply_id

plugin_category = "fun"


@catub.cat_cmd(
    pattern="dark ?(.*)",
    command=("dark", plugin_category),
    info={
        "header": "Fazer a foto ou sticker ficar escura",
        "description": "Fazer a foto ou sticker ficar escura",
        "flags": {
            "d": "Modo morto",
        },
        "usage": [
            "{tr}dark <responda a uma foto ou sticker>",
            "{tr}dark d <responda a uma foto ou sticker>",
        ],
    },
)
async def dark(odi):
    "Cukkkkk"
    if odi.fwd_from:
        return
    await odi.edit("`Em processamento ...`")
    mode = odi.pattern_match.group(1)
    if mode == "d":
        factor = 0.1
    else:
        factor = 0.5
    reply_to_id = await reply_id(odi)
    # ----------------------------------------------------#
    get = await odi.get_reply_message()
    if not get or get.text:
        return await edit_delete(odi, "`Por favor, responda a uma foto/sticker`", 5)
    if get.photo:
        name = "Dark.png"
    elif "tgsticker" in get.media.document.mime_type:
        return await edit_delete(odi, "`Por favor, responda a uma foto/sticker`", 5)
    else:
        name = "Dark.webp"
    # ------------------------------------#
    if get.photo or get.sticker:
        dl = await odi.client.download_media(get)
        img = Image.open(dl)
        bw = img.convert("L")
        enhancer = ImageEnhance.Brightness(bw)
        output = enhancer.enhance(factor)
        output.save(name)
        await odi.client.send_file(odi.chat_id, file=name, reply_to=reply_to_id)
        await odi.delete()
        os.remove(dl)
        os.remove(name)
    else:
        return await edit_delete(odi, "`Por favor, responda a uma foto/sticker`", 5)
