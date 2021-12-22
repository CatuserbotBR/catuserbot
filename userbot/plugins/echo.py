"""
created by @sandy1709
Idea by @BlazingRobonix
"""

from telethon.utils import get_display_name

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.echo_sql import (
    addecho,
    get_all_echos,
    get_echos,
    is_echo,
    remove_all_echos,
    remove_echo,
    remove_echos,
)
from . import get_user_from_event

plugin_category = "fun"


@catub.cat_cmd(
    pattern="addecho$",
    command=("addecho", plugin_category),
    info={
        "header": "Para repetir mensagrns enviadas pelo usuário.",
        "description": "Responda ao usuário desejado com este comando para ter suas mensagens e figurinhas repetidar de volta para ele.",
        "usage": "{tr}addecho <reply>",
    },
)
async def echo(event):
    "Para clonar as mensagens do usuário."
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "`Responda a mensagem de um usuário para clinar suas mensagens`"
        )
    catevent = await edit_or_reply(event, "`Adicionando echo ao usuário...`")
    user, rank = await get_user_from_event(event, catevent, nogroup=True)
    if not user:
        return
    reply_msg = await event.get_reply_message()
    chat_id = event.chat_id
    user_id = reply_msg.sender_id
    if event.is_private:
        chat_name = user.first_name
        chat_type = "Personal"
    else:
        chat_name = get_display_name(await event.get_chat())
        chat_type = "Group"
    user_name = user.first_name
    user_username = user.username
    if is_echo(chat_id, user_id):
        return await edit_or_reply(event, "O usuário ja está ativo com o comando echo.")
    try:
        addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(catevent, f"**Error:**\n`{e}`")
    else:
        await edit_or_reply(catevent, "eae meu chapa")


@catub.cat_cmd(
    pattern="rmecho$",
    command=("rmecho", plugin_category),
    info={
        "header": "Para parar de repetir mensagem particular do usuário.",
        "description": "Responda ao usuário com este comando para parar de repetir suas mensagens de volta.",
        "usage": "{tr}rmecho <reply>",
    },
)
async def echo(event):
    "Para parar de clonar as mensagens do usuário."
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "Responda a uma mensagem do usuário para clonar suas mensagens."
        )
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_echo(chat_id, user_id):
        try:
            remove_echo(chat_id, user_id)
        except Exception as e:
            await edit_delete(catevent, f"**Error:**\n`{e}`")
        else:
            await edit_or_reply(event, "Echo foi parado pelo usuário.")
    else:
        await edit_or_reply(event, "O usuário não está ativado com o echo.")


@catub.cat_cmd(
    pattern="delecho( -a)?",
    command=("delecho", plugin_category),
    info={
        "header": "Para deletar o echo neste chat.",
        "description": "Para parar de clonar as mensagens dos usuários no particular ou em todos os chats.",
        "flags": {"a": "To stop in all chats"},
        "usage": [
            "{tr}delecho",
            "{tr}delecho -a",
        ],
    },
)
async def echo(event):
    "Para deletar o echo neste chat."
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_echos()
        if len(lecho) == 0:
            return await edit_delete(
                event, "Você não ativou nenhum echo com pelo menos um usuário em pelo menos um chat."
            )
        try:
            remove_all_echos()
        except Exception as e:
            await edit_delete(event, f"**Error:**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(
                event, "Echo deletado para todos os usuários ativos em todos os chats."
            )
    else:
        lecho = get_echos(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "Você não ativou o echo para pelo menos um usuário neste chat."
            )
        try:
            remove_echos(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**Error:**\n`{e}`", 10)
        else:
            await edit_or_reply(
                event, "Echo deletado para todos os usuários ativos neste chat."
            )


@catub.cat_cmd(
    pattern="listecho( -a)?$",
    command=("listecho", plugin_category),
    info={
        "header": "Mostra a lista de usuários para os quais voce habilitou.",
        "flags": {
            "a": "Listar todos users com echo em todos os chats.",
        },
        "usage": [
            "{tr}listecho",
            "{tr}listecho -a",
        ],
    },
)
async def echo(event):  # sourcery no-metrics
    "Para listar todos os usuários que você ativou o echo."
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**Echo enabled users:**\n\n"
    if input_str:
        lsts = get_all_echos()
        group_chats = ""
        if len(lsts) <= 0:
            return await edit_or_reply(event, "Nao tem usuários ativo com echo.")
        for echos in lsts:
            if echos.chat_type == "Personal":
                if echos.user_username:
                    private_chats += (
                        f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                    )
                else:
                    private_chats += (
                        f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                    )
            elif echos.user_username:
                group_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"
            else:
                group_chats += f"☞ [{echos.user_name}](tg://user?id={echos.user_id}) in chat {echos.chat_name} of chat id `{echos.chat_id}`\n"

        if private_chats != "":
            output_str += "**Private Chats**\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**Group Chats**\n" + group_chats
    else:
        lsts = get_echos(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(
                event, "Nao há echo ativo com nenhum usuário neste chat."
            )

        for echos in lsts:
            if echos.user_username:
                private_chats += (
                    f"☞ [{echos.user_name}](https://t.me/{echos.user_username})\n"
                )
            else:
                private_chats += (
                    f"☞ [{echos.user_name}](tg://user?id={echos.user_id})\n"
                )
        output_str = "**Usuários ativos com o echo neste chat são:**\n" + private_chats

    await edit_or_reply(event, output_str)


@catub.cat_cmd(incoming=True, edited=False)
async def samereply(event):
    if is_echo(event.chat_id, event.sender_id) and (
        event.message.text or event.message.sticker
    ):
        await event.reply(event.message)
