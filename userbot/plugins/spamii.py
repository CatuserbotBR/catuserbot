
from userbot import catub
from ..core.managers import edit_delete
from ..helpers.utils import reply_id

plugin_category = "extra"

@catub.cat_cmd(
    pattern="gcast?(.*)",
    command=("gcast", plugin_category),
    info={
        "header": " Para enviar a mensagem para todos os grupos que voce está (olha o ban, moço)",
        "usage": [
            "{tr}gcast <seu texto>",
        ],
    },
)
async def xd(event):
    await event.edit("enviando...")
    themessage = event.pattern_match.group(1)
    async for cat in borg.iter_dialogs():
        lol = 0
        done = 0
        if cat.is_group:
            chat = cat.id
            try:
                await bot.send_message(chat, f"{themessage}")
                done += 1
            except:
                lol += 1
                pass
    await event.reply(f"Feito em {done} chats, erro em {lol} chat(s)")
