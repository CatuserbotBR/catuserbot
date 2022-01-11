from userbot import catub

from ..core.managers import edit_delete
from ..helpers.utils import reply_id

plugin_category = "extra"


@catub.cat_cmd(
    pattern="letra ?(.*)",
    command=("letra", plugin_category),
    info={
        "header": "Envia a letra [inline] de uma música junto com os links do Spotify e Youtube\n•Adicione o nome do artista se você obtiver letras diferentes\n•você também pode digitar uma linha de uma música para pesquisar",
        "usage": [
            "{tr}letra <nome da música>",
            "{tr}letra <nome da música - artista>",
        ],
    },
)
async def GayIfUChangeCredit(event):
    "Lyrics Time"
    if event.fwd_from:
        return
    bot = "@ilyricsbot"
    song = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not song:
        return await edit_delete(event, "`Coloque uma música`", 15)
    await event.delete()
    results = await event.client.inline_query(bot, song)
    await results[0].click(event.chat_id, reply_to=reply_to_id)
