from .. import catub
from ..core.managers import edit_or_reply

plugin_category = "tools"


@catub.cat_cmd(
    pattern="shift (.*)",
    command=("shift", plugin_category),
    info={
        "header": "Copiar canal/grupo",
        "description": "Para copiar todas as mensagens/arquivos de um canal/grupo para seu canal/grupo",
        "usage": "{tr}shift <id do grupo/canal de origem> | <id do grupo/canal de destino>",
        "examples": "{tr}shift -100|-100",
    },
)
async def _(e):
    x = e.pattern_match.group(1)
    z = await edit_or_reply(e, "em processamento...")
    a, b = x.split("|")
    try:
        c = int(a)
    except Exception:
        try:
            c = (await bot.get_entity(a)).id
        except Exception:
            await z.edit("Canal fornecido inválido")
            return
    try:
        d = int(b)
    except Exception:
        try:
            d = (await bot.get_entity(b)).id
        except Exception:
            await z.edit("Canal fornecido inválido")
            return
    async for msg in bot.iter_messages(int(c), reverse=True):
        try:
            await asyncio.sleep(1.5)
            await bot.send_message(int(d), msg)
        except BaseException:
            pass
    await z.edit("Done")
