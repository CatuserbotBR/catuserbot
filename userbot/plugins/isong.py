#By @awtfg
from userbot import catub
from ..core.managers import edit_delete
from ..helpers.utils import reply_id

plugin_category = "utils"

async def isong(event, text):
    if event.fwd_from:
        return
    bot = "@LyBot"
    if not text:
        await edit_delete(event, "`Coloque o nome de uma música`")
    else:
        await edit_or_reply(event, "`Pesquisando...`")
        try:
            run = await event.client.inline_query(bot, text)
            result = await run[0].click("me")
        except IndexError as error:
            result = ""
    return result

@catub.cat_cmd(
    pattern="isong ?(.*)",
    command=("isong", plugin_category),
    info={
        "header": "Download de música",
        "usage": [
            "{tr}isong <nome de música>",
        ],
    },
)
async def _(event):
    reply_to_id = await reply_id(event)
    text = event.pattern_match.group(1)
    result = await isong(event, text)
    if result == "":
        return await event.edit("`Música não encontrada`")
    else:
        await event.delete()
        await event.client.send_file(event.chat_id, result, caption=f"", reply_to=reply_to_id)
        await result.delete()
