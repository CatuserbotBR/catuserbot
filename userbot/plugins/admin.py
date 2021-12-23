from asyncio import sleep

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "`A imagem é muito pequena`"
PP_ERROR = "`Falha ao processar a imagem`"
NO_ADMIN = "`Eu não sou um admin noob zé roela!`"
NO_PERM = "`Eu não tenho permissões suficientes! Isso é tão sedutor. Alexa toque despacito`"
CHAT_PP_CHANGED = "`Imagem do bate-papo alterada`"
INVALID_MEDIA = "`Extensão inválida`"

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

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

plugin_category = "admin"
# ================================================


@catub.cat_cmd(
    pattern="gpic( -s| -d)$",
    command=("gpic", plugin_category),
    info={
        "cabeçalho": "Para alterar a imagem de perfil do grupo ou excluir a imagem de perfil do grupo",
        "descrição": "Responder à imagem para alterar a imagem de perfil do grupo",
        "flags": {
            "-s": "Para definir a foto do grupo",
            "-d": "Para excluir a foto do grupo",
        },
        "uso": [
            "{tr}gpic -s <responder a imagem>",
            "{tr}gpic -d",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "Para alterar o Grupo dp"
    flag = (event.pattern_match.group(1)).strip()
    if flag == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await edit_delete(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await edit_delete(event, CHAT_PP_CHANGED)
            except PhotoCropSizeSmallError:
                return await edit_delete(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await edit_delete(event, PP_ERROR)
            except Exception as e:
                return await edit_delete(event, f"**Error : **`{str(e)}`")
            process = "Atualizado"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await edit_delete(event, f"**Error : **`{e}`")
        process = "Apagado"
        await edit_delete(event, "```foto do perfil do grupo excluída com sucesso.```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GROUPPIC\n"
            f"Foto do perfil do grupo {process} com sucesso "
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="promote(?:\s|$)([\s\S]*)",
    command=("promote", plugin_category),
    info={
        "cabeçalho": "Para dar direitos de administrador a uma pessoa",
        "descrição": "Concede direitos de administrador para a pessoa no bate-papo\
            \nNote : Você precisa de direitos adequados para isso",
        "uso": [
            "{tr}promote <userid/username/reply>",
            "{tr}promote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "Para promover uma pessoa no chat"
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Admin"
    if not user:
        return
    catevent = await edit_or_reply(event, "`Promovendo...`")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("`Promovido com sucesso! Agora faça sua parte`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PROMOTE\
            \nUSER: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="demote(?:\s|$)([\s\S]*)",
    command=("demote", plugin_category),
    info={
        "cabeçalho": "Para remover uma pessoa da lista de administradores",
        "descrição": "Remove todos os direitos de administrador dessa pessoa no bate-papo\
            \nNote : Você precisa de direitos adequados para isso e também deve ser o proprietário ou administrador que promoveu o corno",
        "uso": [
            "{tr}demote <userid/username/reply>",
            "{tr}demote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "Para rebaixar uma pessoa no grupo"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "`Rebaixando...`")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "admin"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    await catevent.edit("`Rebaixado com sucesso! Faz o trabalho direito na próxima vez corno`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#DEMOTE\
            \nUSER: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="ban(?:\s|$)([\s\S]*)",
    command=("ban", plugin_category),
    info={
        "cabeçalho": "Irá banir o corno do grupo onde você usou este comando.",
        "descrição": "O removerá permanentemente deste grupo e ele não poderá voltar a entrar no grupo\
            \nNote : Você precisa de direitos adequados para isso.",
        "uso": [
            "{tr}ban <userid/username/reply>",
            "{tr}ban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "Para banir uma pessoa no grupo"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await edit_delete(event, "__Você não pode se banir.__")
    catevent = await edit_or_reply(event, "`Acabando com a praga!`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await catevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await catevent.edit(
            "`Eu não tenho direitos de detonação de mensagens! Mas ele ainda está banido!`"
        )
    if reason:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)}` está banido !!`\n**Motivo : **`{reason}`"
        )
    else:
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `está banido !!`"
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nUSER: [{user.first_name}](tg://user?id={user.id})\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nREASON : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nUSER: [{user.first_name}](tg://user?id={user.id})\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@catub.cat_cmd(
    pattern="unban(?:\s|$)([\s\S]*)",
    command=("unban", plugin_category),
    info={
        "cabeçalho": "Desbanirá o cara do grupo onde você usou este comando.",
        "descrição": "Remove a conta do usuário da lista de banidos do grupo\
            \nNote : Você precisa de direitos adequados para isso.",
        "usage": [
            "{tr}unban <userid/username/reply>",
            "{tr}unban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "Para desbanir uma pessoa"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "`Desbanindo...`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `Desbanido com sucesso. Se der mole de novo é vapo.`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("`Uou minha lógica de desbanimento quebrou!`")
    except Exception as e:
        await catevent.edit(f"**Error :**\n`{e}`")


@catub.cat_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@catub.cat_cmd(
    pattern="mute(?:\s|$)([\s\S]*)",
    command=("mute", plugin_category),
    info={
        "cabeçalho": "Para impedir que o usuário mencionado envie mensagens",
        "descrição": "Se não for admin, então mude sua permissão no grupo,\
            se ele for administrador ou se você tentar no chat pessoal, as mensagens dele serão deletadas\
            \nNote : Você precisa de direitos adequados para isso.",
        "uso": [
            "{tr}mute <userid/username/reply>",
            "{tr}mute <userid/username/reply> <reason>",
        ],
    },  # sourcery no-metrics
)
async def startmute(event):
    "Para silenciar uma pessoa naquele bate-papo específico"
    if event.is_private:
        await event.edit("`Pode ter ocorrido problemas inesperados ou erros feios!`")
        await sleep(2)
        await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "`Este usuário já está silenciado neste bate-papo ~~kkkkkkk triste parcero~~`"
            )
        if event.chat_id == catub.uid:
            return await edit_delete(event, "`Você não pode se silenciar`")
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**Error **\n`{e}`")
        else:
            await event.edit("`Essa pessoa foi silenciada com sucesso. Faz silêncio ai parcero.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"**User :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await edit_or_reply(
                event, "`Você não pode silenciar uma pessoa sem direitos de administrador.` ಥ﹏ಥ  "
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == catub.uid:
            return await edit_or_reply(event, "`Desculpe, eu não consigo me silenciar`")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "`Este usuário já está silenciado neste bate-papo ~~kkkkkkk triste parcero~~`"
            )
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await edit_or_reply(
                    event,
                    "`Este usuário já está silenciado neste bate-papo ~~kkkkkkk triste parcero~~`",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{e}`")
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "`Você não pode silenciar uma pessoa se não tiver permissão para excluir mensagens. ಥ﹏ಥ`",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "`Você não pode silenciar uma pessoa sem direitos de administrador.` ಥ﹏ಥ  "
                )
            mute(user.id, event.chat_id)
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{e}`")
        if reason:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `está silenciado em {get_display_name(await event.get_chat())}`\n"
                f"`Motivo:`{reason}",
            )
        else:
            await edit_or_reply(
                event,
                f"{_format.mentionuser(user.first_name ,user.id)} `está silenciado em {get_display_name(await event.get_chat())}`\n",
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@catub.cat_cmd(
    pattern="unmute(?:\s|$)([\s\S]*)",
    command=("unmute", plugin_category),
    info={
        "cabeçalho": "Para permitir que o usuário envie mensagens novamente",
        "descrição": "Irá alterar as permissões do usuário no grupo para enviar mensagens novamente.\
        \nNote : Você precisa de direitos adequados para isso.",
        "uso": [
            "{tr}unmute <userid/username/reply>",
            "{tr}unmute <userid/username/reply> <reason>",
        ],
    },
)
async def endmute(event):
    "Para silenciar uma pessoa naquele bate-papo específico"
    if event.is_private:
        await event.edit("`Pode ter ocorrido problemas inesperados ou erros feios!`")
        await sleep(1)
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "`__Este usuário não está silenciado neste chat__\n（ ^_^）o自自o（^_^ ）`"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**Error **\n`{e}`")
        else:
            await event.edit(
                "`Desmutou essa pessoa com sucesso\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_UNMUTE\n"
                f"**User :** [{replied_user.user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client.get_permissions(event.chat_id, user.id)
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await edit_or_reply(
                event,
                "`Este usuário já pode falar livremente neste chat ~~fica esperto se não o mute canta de novo~~`",
            )
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{e}`")
        await edit_or_reply(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} `não está silenciado em {get_display_name(await event.get_chat())}\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@catub.cat_cmd(
    pattern="kick(?:\s|$)([\s\S]*)",
    command=("kick", plugin_category),
    info={
        "cabeçalho": "Para expulsar uma pessoa do grupo",
        "descrição": "Expulsará o usuário do grupo para que ele possa voltar.\
        \nNote : Você precisa de direitos adequados para isso.",
        "uso": [
            "{tr}kick <userid/username/reply>",
            "{tr}kick <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    "use isso para expulsar um usuário do chat"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    catevent = await edit_or_reply(event, "`Expulsando...`")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await catevent.edit(NO_PERM + f"\n{e}")
    if reason:
        await catevent.edit(
            f"`Expulsado` [{user.first_name}](tg://user?id={user.id})`!`\nMotivo: {reason}"
        )
    else:
        await catevent.edit(f"`Expulsado` [{user.first_name}](tg://user?id={user.id})`!`")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@catub.cat_cmd(
    pattern="pin( loud|$)",
    command=("pin", plugin_category),
    info={
        "cabeçalho": "Para fixar mensagens no bate-papo",
        "descrição": "Responda a uma mensagem para fixá-la no bate-papo\
        \nNote : Você precisa de direitos adequados para isso se quiser usar em grupo.",
        "opções": {"loud": "Para não notificar a galera . Fixará silenciosamente"},
        "uso": [
            "{tr}pin <reply>",
            "{tr}pin loud <reply>",
        ],
    },
)
async def pin(event):
    "Para fixar uma mensagem no bate-papo"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "`Responda a uma mensagem para fixá-la.`", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "`Fixado com sucesso!`", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PIN\
                \n__fixou com sucesso uma mensagem no chat__\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nLOUD: {is_silent}",
        )


@catub.cat_cmd(
    pattern="unpin( all|$)",
    command=("unpin", plugin_category),
    info={
        "cabeçalho": "Para desfixar mensagens no bate-papo",
        "descrição": "Responda a uma mensagem para desfixa-lá no bate-papo\
        \nNote : Você precisa de direitos adequados para isso se quiser usar em grupo.",
        "opções": {"all": "Para desfixar todas as mensagens no bate-papo"},
        "uso": [
            "{tr}unpin <reply>",
            "{tr}unpin all",
        ],
    },
)
async def pin(event):
    "Para desfixar mensagem(s) no grupo"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edit_delete(
            event,
            "__Responda a uma mensagem para desfixa-lá ou usar __`.unpin all`__ para desfixar todas__",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event, "`Responda a uma mensagem para desfixa-lá ou usar .unpin all`", 5
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "`Desafixado com sucesso!`", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#UNPIN\
                \n__mensagem(s) desfixado com sucesso no bate-papo__\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@catub.cat_cmd(
    pattern="undlt( -u)?(?: |$)(\d*)?",
    command=("undlt", plugin_category),
    info={
        "cabeçalho": "Para obter mensagens excluídas recentes no grupo",
        "descrição": "Para verificar as mensagens excluídas recentemente no grupo, por padrão, exibirá 5. você pode receber de 1 a 15 mensagens.",
        "flags": {
            "u": "use está flag para fazer upload de mídia para bate-papo, caso contrário, será apenas mostrado como mídia."
        },
        "uso": [
            "{tr}undlt <count>",
            "{tr}undlt -u <count>",
        ],
        "exemplos": [
            "{tr}undlt 7",
            "{tr}undlt -u 7 (isto irá responder a todas as 7 mensagens a esta mensagem",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "Para verificar as mensagens apagadas recentes no grupo"
    catevent = await edit_or_reply(event, "`Pesquisando ações recentes .....`")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**Recentes {lim} As mensagens excluídas neste grupo são :**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **Enviado por** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **Enviado por** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(catevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(catevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**Enviado por** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**Enviado por** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
