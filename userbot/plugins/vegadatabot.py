import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import catub
from ..core.managers import edit_delete, edit_or_reply
plugin_category = "utils"


@catub.cat_cmd(
    pattern="d(?:\s|$)([\s\S]*)",
    command=("d", plugin_category),
    info={
        "header": "Para pesquisar as specs de um celular",
        "description": "Veja as specs de um celular",
        "usage": "{tr}d <celular>",
    },
)
async def _(event):  # sourcery no-metrics
    "Vê spec de um celular"
    input_str = event.pattern_match.group(1)
    if not input_str:
        await edit_delete(
            event,
            "`coloca um celular arrombado`",
        )
        return
    device_ = input_str
    catevent = await edit_or_reply(event, "`Pesquisando...`")
    async with event.client.conversation("@vegadata_bot") as conv:
        try:
            msg = await conv.send_message(f"!d {device_}")
        except YouBlockedUserError:
            await catevent.edit("```Desbloqueie @vegadata_bot.```")
            return
        response = await conv.get_response()
        await edit_or_reply(catevent,response.text, link_preview=True)
    await event.client.delete_messages(conv.chat_id, [msg.id, response.id])
