from telethon.utils import pack_bot_file_id

from userbot import catub
from userbot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

LOGS = logging.getLogger(__name__)


@catub.cat_cmd(
    pattern="(get_id|id)(?:\s|$)([\s\S]*)",
    command=("id", plugin_category),
    info={
        "header": "Para pegar o id do grupo ou do usuárioTo get id of the group or user.",
        "description": "se for dada entrada então mostra o id daquele dado chat/canal/usuário senão se você responder ao usuário então mostra o id do usuário respondido. \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <resposta/nome do usuário>",
    },
)
async def _(event):
    "Para ter o id do grupo ou do usuário."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"O ID do usuário `{input_str}` é `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"O ID do chat/canal `{p.title}` é `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "`Forneça a entrada como nome de usuário ou responda ao usuário.`")
    elif event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"**ID do chat: **`{event.chat_id}`\n**Do ID do usuário: **`{r_msg.sender_id}`\n**ID do arquivo de mídia: **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                event,
                f"**ID do chat atual ID: **`{event.chat_id}`\n**Do ID do usuário: **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(event, f"**ID do chat atual: **`{event.chat_id}`")
