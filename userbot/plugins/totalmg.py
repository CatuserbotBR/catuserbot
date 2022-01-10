from . import catub
from ..core.managers import edit_or_reply
plugin_category = "fun"
@catub.cat_cmd(
    pattern="totalmsgs ?(.*)",
    command=("totalmsgs", plugin_category),
    info={
        "header": "Retorna sua contagem total de mensagens ou de qualquer usuário no chat atual",
        "usage": "{tr}totalmsgs [nome do usuário]/<resposta>/nada",
    },
)
async def _(e):
    match = e.pattern_match.group(1)
    if match:
        user = match
    elif e.is_reply:
        user = (await e.get_reply_message()).sender_id
    else:
        user = "me"
    a = await e.client.get_messages(e.chat_id, 0, from_user=user)
    user = await e.client.get_entity(user)
    await edit_or_reply(e, f"Total de mensagens de `{user.first_name}`\n**Aqui :** `{a.total}`")
