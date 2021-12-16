import random

from telethon.utils import get_display_name

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import get_user_from_event, rs_client
from ..sql_helper.chatbot_sql import (
    addai,
    get_all_users,
    get_users,
    is_added,
    remove_ai,
    remove_all_users,
    remove_users,
)
from ..sql_helper.globals import gvarstatus

plugin_category = "fun"

tired_response = [
    "Estou um pouco cansado, por favor me dê um pouco de descanso.",
    "Quem é você para me fazer perguntas continuamente?",
    "Me deixe sozinho por alguns momentos.",
    "Hora de dormir, eu entrarei em contato com você em breve.",
    "Eu tenho um trabalho a fazer, volte mais tarde.",
    "Eu preciso descansar, me deixa sozinho por um tempo.",
    "Não estou me sentindo bem, por favor volte mais tarde.",
]


@catub.cat_cmd(
    pattern="addai$",
    command=("addai", plugin_category),
    info={
        "header": "Para adicionar AI chatbot à conta respondida.",
        "usage": "{tr}addai <resposta>",
    },
)
async def add_chatbot(event):
    "Para habilitar AI para a pessoa respondida"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "`Responda a uma mensagem de um usuário para ativar o AI.`"
        )
    catevent = await edit_or_reply(event, "`Adicionando AI ao usuário...`")
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
    if is_added(chat_id, user_id):
        return await edit_or_reply(event, "`O usuário já está habilitado com AI.`")
    try:
        addai(chat_id, user_id, chat_name, user_name, user_username, chat_type)
    except Exception as e:
        await edit_delete(catevent, f"**Erro:**\n`{e}`")
    else:
        await edit_or_reply(catevent, "Olá")


@catub.cat_cmd(
    pattern="rmai$",
    command=("rmai", plugin_category),
    info={
        "header": "Para parar AI para as mensagens desse usuário.",
        "usage": "{tr}rmai <resposta>",
    },
)
async def remove_chatbot(event):
    "Para parar AI para aquele usuário"
    if event.reply_to_msg_id is None:
        return await edit_or_reply(
            event, "Responda a uma mensagem do usuário para impedir AI nele."
        )
    reply_msg = await event.get_reply_message()
    user_id = reply_msg.sender_id
    chat_id = event.chat_id
    if is_added(chat_id, user_id):
        try:
            remove_ai(chat_id, user_id)
        except Exception as e:
            await edit_delete(catevent, f"**Erro:**\n`{e}`")
        else:
            await edit_or_reply(event, "AI foi interrompido para o usuário.")
    else:
        await edit_or_reply(event, "O usuário não está ativado com AI.")


@catub.cat_cmd(
    pattern="delai( -a)?",
    command=("delai", plugin_category),
    info={
        "header": "Para deletar AI desse chat.",
        "description": "Para parar AI para todos os usuários habilitados neste chat apenas ..",
        "flags": {"a": "Para parar em todos os chats"},
        "usage": [
            "{tr}delai",
            "{tr}delai -a",
        ],
    },
)
async def delete_chatbot(event):
    "Para deletar AI desse chat."
    input_str = event.pattern_match.group(1)
    if input_str:
        lecho = get_all_users()
        if len(lecho) == 0:
            return await edit_delete(
                event, "Você não habilitou AI para pelo menos um usuário em nenhum chat."
            )
        try:
            remove_all_users()
        except Exception as e:
            await edit_delete(event, f"**Erro:**\n`{str(e)}`", 10)
        else:
            await edit_or_reply(event, "AI excluída para todos os usuários habilitados em todos os chats.")
    else:
        lecho = get_users(event.chat_id)
        if len(lecho) == 0:
            return await edit_delete(
                event, "Você não habilitou AI para pelo menos um usuário neste chat."
            )
        try:
            remove_users(event.chat_id)
        except Exception as e:
            await edit_delete(event, f"**Erro:**\n`{e}`", 10)
        else:
            await edit_or_reply(event, "AI excluída para todos os usuários habilitados neste chat")


@catub.cat_cmd(
    pattern="listai( -a)?$",
    command=("listai", plugin_category),
    info={
        "header": "mostra a lista de usuários para os quais você habilitou AI",
        "flags": {
            "a": "Para listar usuários habilitados para AI em todos os chats",
        },
        "usage": [
            "{tr}listai",
            "{tr}listai -a",
        ],
    },
)
async def list_chatbot(event):  # sourcery no-metrics
    "Para listar todos os usuários nos quais você ativou a AI."
    input_str = event.pattern_match.group(1)
    private_chats = ""
    output_str = "**Usuários habilitados para AI:**\n\n"
    if input_str:
        lsts = get_all_users()
        group_chats = ""
        if len(lsts) <= 0:
            return await edit_or_reply(event, "Não há usuários habilitados para AI")
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
                group_chats += f"☞ [{echos.user_name}](https://t.me/{echos.user_username}) no bate-papo {echos.chat_name} de id `{echos.chat_id}`\n"
            else:
                group_chats += f"☞ [{echos.user_name}](tg://user?id={echos.user_id}) no bate-papo {echos.chat_name} de id de `{echos.chat_id}`\n"

        if private_chats != "":
            output_str += "**Chats Privados**\n" + private_chats + "\n\n"
        if group_chats != "":
            output_str += "**Bate-papos em grupo**\n" + group_chats
    else:
        lsts = get_users(event.chat_id)
        if len(lsts) <= 0:
            return await edit_or_reply(
                event, "Não há usuários habilitados para AI neste chat"
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
        output_str = "**Os usuários habilitados para AI neste chat são:**\n" + private_chats
    await edit_or_reply(event, output_str)


@catub.cat_cmd(incoming=True, edited=False)
async def ai_reply(event):
    if is_added(event.chat_id, event.sender_id) and (event.message.text):
        AI_LANG = gvarstatus("AI_LANG") or "en"
        master_name = get_display_name(await event.client.get_me())
        try:
            response = await rs_client.get_ai_response(
                message=event.message.text,
                server="primary",
                master="CatUserbot",
                bot=master_name,
                uid=event.client.uid,
                language=AI_LANG,
            )
            await event.reply(response.message)
        except Exception as e:
            LOGS.error(str(e))
            await event.reply(random.choice(tired_response))
