import asyncio
from datetime import datetime

from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format
from ..sql_helper import gban_sql_helper as gban_sql
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event

plugin_category = "admin"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


@catub.cat_cmd(
    pattern="gban(?:\s|$)([\s\S]*)",
    command=("gban", plugin_category),
    info={
        "header": "Para banir o usuário em todos os grupos que você for admin.",
        "description": "Irá banir a pessoa em todos os grupos que você for admin apenas.",
        "usage": "{tr}gban <username/reply/userid> <reason (optional)>",
    },
)
async def catgban(event):  # sourcery no-metrics
    "Para banir usuário em todos os grupos que você for admin."
    cate = await edit_or_reply(event, "`gbanindo.......`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == catub.uid:
        return await edit_delete(cate, "`por que caralhos eu me baniria?")
    if gban_sql.is_gbanned(user.id):
        await cate.edit(
            f"`O `[user](tg://user?id={user.id})` ja esta na lista de gbanidos mas de qualquer forma checando novamente.`"
        )
    else:
        gban_sql.catgban(user.id, reason)
    san = await admin_groups(event.client)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "`Voce não é admin de pelo menos um grupo.` ")
    await cate.edit(
        f"`Iniciando gban do `[user](tg://user?id={user.id}) `em {len(san)} grupos`"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`Você não tem a permissão necessária em:`\n**Chat :** {get_display_name(achat)}(`{achat.id}`)\n`para banir aqui.`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `Foi gbanido em {count} grupos em {cattaken} segundos`!!\n**Motivo :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `Foi gbanido em {count} grupos em {cattaken} segundos`!!"
        )
    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Motivo :** `{reason}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GBAN\
                \nGlobal Ban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Banned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            pass


@catub.cat_cmd(
    pattern="ungban(?:\s|$)([\s\S]*)",
    command=("ungban", plugin_category),
    info={
        "header": "Para desbanir a pessoa em todos os grupos que você for admin.",
        "description": "Irá desbanir e também remover da lista de gbanidos.",
        "usage": "{tr}ungban <username/reply/userid>",
    },
)
async def catgban(event):
    "Para desbanir a pessoa de todos os grupos que você for admin."
    cate = await edit_or_reply(event, "`Desbanindo.....`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        return await edit_delete(
            cate, f"O [user](tg://user?id={user.id}) `não esta na sua lista de gbanidos.`"
        )
    san = await admin_groups(event.client)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "`Você não é admin de pelo menos um grupo. `")
    await cate.edit(
        f"Iniciando desgbanimento do usuário [user](tg://user?id={user.id}) em `{len(san)}` grupos"
    )
    for i in range(sandy):
        try:
            await event.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`Você não tem a permissão necessária em :`\n**Chat :** {get_display_name(achat)}(`{achat.id}`)\n`Para desbanir aqui.`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}`) `Foi desgbanido em {count} grupos em {cattaken} segundos`!!\n**Motivo :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `Foi desgbanido em {count} grupos em {cattaken} segundos`!!"
        )

    if BOTLOG and count != 0:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Motivo :** `{reason}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#UNGBAN\
                \nGlobal Unban\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Unbanned in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )


@catub.cat_cmd(
    pattern="listgban$",
    command=("listgban", plugin_category),
    info={
        "header": "Mostra a lista de todos gbanidos por você.",
        "usage": "{tr}listgban",
    },
)
async def gablist(event):
    "Mostra a lista de todos usuários gbanidos por você."
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Lista de GBanidos\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) para {a_user.reason}\n"
            else:
                GBANNED_LIST += (
                    f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) sem reação\n"
                )
    else:
        GBANNED_LIST = "Nao há usuários gbanidos (ainda)"
    await edit_or_reply(event, GBANNED_LIST)


@catub.cat_cmd(
    pattern="gmute(?:\s|$)([\s\S]*)",
    command=("gmute", plugin_category),
    info={
        "header": "Para mutar a pessoa em todos ls grupos que você for admin.",
        "description": "Isto nao muda as permissões do usuário mas irá deletar todas as mensagens enviadas por ele nos grupos que você for admin incluindo chats privados.",
        "usage": "{tr}gmute username/reply> <reason (optional)>",
    },
)
async def startgmute(event):
    "Para mutar a pessoa em todos os grupos que você for admin."
    if event.is_private:
        await event.edit("`Erros foram cometidos, não sabe usar nem um comando?`")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "`Desculpa, mas parece ser uma idéia estúpida me gmutar.`")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "`Desculpe. Eu não consigo buscar o usuário.`")
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} `já esta gmutado.`",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**Error**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `esta gmutado, finalmente silêncio...`\n**Motivo :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `esta gmutado, finalmente silêncio..`",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**Usuário :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**Motivo :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"**Usuário : ** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@catub.cat_cmd(
    pattern="ungmute(?:\s|$)([\s\S]*)",
    command=("ungmute", plugin_category),
    info={
        "header": "Para desmitar a pessoa em todos os grupos que você for admin.",
        "description": "Isto irá apenas funcionar nse você mutou a pessoa pelo seu comando de gmute.",
        "usage": "{tr}ungmute <username/reply>",
    },
)
async def endgmute(event):
    "Para remover o gmute da pessoa."
    if event.is_private:
        await event.edit("`Erros foram cometidos, serio que voce nao sabe nem usar este comando simples?`")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "`Desculpe, mas não consigo me desmutar.`")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(event, "`Desculpe. Eu não consigo buscar o usuário.`")
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event, f"{_format.mentionuser(user.first_name ,user.id)} `não esta gmutado`"
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**Error**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `não está gmutado infelizmente  `\n**Motivo :** `{reason}`",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `não está gmutado infelizmente`",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**Usuário :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**Motivo :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"**Usuário :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@catub.cat_cmd(
    pattern="gkick(?:\s|$)([\s\S]*)",
    command=("gkick", plugin_category),
    info={
        "header": "Kicka a pessoa em todos os grupos que você é admin.",
        "usage": "{tr}gkick <username/reply/userid> <reason (optional)>",
    },
)
async def catgkick(event):  # sourcery no-metrics
    "Kicka a pessoa em todos os grupos que você for admin."
    cate = await edit_or_reply(event, "`removendo.......`")
    start = datetime.now()
    user, reason = await get_user_from_event(event, cate)
    if not user:
        return
    if user.id == catub.uid:
        return await edit_delete(cate, "`Por que eu me kickaria? isto parece estúpido.`")
    san = await admin_groups(event.client)
    count = 0
    sandy = len(san)
    if sandy == 0:
        return await edit_delete(cate, "`Você não é admin de pelo menos um grupo` ")
    await cate.edit(
        f"`Iniciando gkick do `[user](tg://user?id={user.id}) `em {len(san)} grupos`"
    )
    for i in range(sandy):
        try:
            await event.client.kick_participant(san[i], user.id)
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            achat = await event.client.get_entity(san[i])
            await event.client.send_message(
                BOTLOG_CHATID,
                f"`Você não tem as permissões necessárias em :`\n**Chat :** {get_display_name(achat)}(`{achat.id}`)\n`Para Kickar o usuário de la`",
            )
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `foi gckickado em {count} Nos grupos {cattaken} segundos`!!\n**Motivo :** `{reason}`"
        )
    else:
        await cate.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `Foi gckickado em {count} grupos em {cattaken} segundos`!!"
        )

    if BOTLOG and count != 0:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n**Motivo :** `{reason}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#GKICK\
                \nGlobal Kick\
                \n**User : **[{user.first_name}](tg://user?id={user.id})\
                \n**ID : **`{user.id}`\
                \n__Kicked in {count} groups__\
                \n**Time taken : **`{cattaken} seconds`",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)
