import asyncio
from datetime import datetime

from telethon.tl import functions, types

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import _format
from . import BOTLOG, BOTLOG_CHATID
import random 
plugin_category = "utils"

LOGS = logging.getLogger(__name__)


class AFK:
    def __init__(self):
        self.USERAFK_ON = {}
        self.afk_time = None
        self.last_afk_message = {}
        self.afk_star = {}
        self.afk_end = {}
        self.reason = None
        self.msg_link = False
        self.afk_type = None
        self.media_afk = None
        self.afk_on = False


AFK_ = AFK()

AFK1MOD = [
    "Agora estou ocupado. Por favor, fale em uma bolsa e quando eu voltar você pode apenas me dar a bolsa!",
    "Estou fora agora. Se precisar de alguma coisa, deixe mensagem após o beep:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "Volto em alguns minutos e se não ..,\nespere mais um pouco.",
    "Não estou aqui agora, então provavelmente estou em outro lugar.",
    "Sei que quer falar comigo, mas estou ocupado salvando o mundo agora.",
    "Às vezes, vale a pena esperar pelas melhores coisas da vida…\nEstou ausente então espere por mim.",
    "Olá, seja bem-vindo à minha mensagem de ausência, como posso ignorá-lo hoje?",
    "Estou mais longe que 7 mares e 7 países,\n7 águas e 7 continentes,\n7 montanhas e 7 colinas,\n7 planícies e 7 montes,\n7 piscinas e 7 lagos,\n7 nascentes e 7 prados,\n7 cidades e 7 bairros,\n7 quadras e 7 casas...\n\nOnde nem mesmo suas mensagens podem me alcançar!",
    "Estou ausente no momento, mas se você gritar alto o suficiente na tela, talvez eu possa ouvir você.",
    "Por favor, deixe uma mensagem e me faça sentir ainda mais importante do que já sou.",
    "Eu não estou aqui então pare de escrever para mim,\nou então você se verá com uma tela cheia de suas próprias mensagens.",
    "Se eu estivesse aqui,\nEu te diria onde estou.\n\nMas eu não estou,\nentão me pergunte quando eu voltar...",
    "Não estou disponível agora, por favor, deixe seu nome, número e endereço e eu irei persegui-lo mais tarde. ",
    "Desculpe, eu não estou aqui agora.\nSinta-se à vontade para falar com meu userbot pelo tempo que desejar.\nEu respondo mais tarde.",
    "A vida é tão curta, há tantas coisas para fazer...\nEstou ausente fazendo uma delas...",
    "Eu não estou aqui agora...\nmas se estivesse...\n\nisso não seria incrível?",
]

@catub.cat_cmd(outgoing=True, edited=False)
async def set_not_afk(event):
    if AFK_.afk_on is False:
        return
    back_alive = datetime.now()
    AFK_.afk_end = back_alive.replace(microsecond=0)
    if AFK_.afk_star != {}:
        total_afk_time = AFK_.afk_end - AFK_.afk_star
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d, {h}h, {m}m, {s}s."
        elif h > 0:
            endtime += f"{h}h, {m}m, {s}s."
        else:
            endtime += f"{m}m, {s}s." if m > 0 else f"{s}s."
    current_message = event.message.message
    if (("afk" not in current_message) or ("#afk" not in current_message)) and (
        "on" in AFK_.USERAFK_ON
    ):
        shite = await event.client.send_message(
            event.chat_id,
            "**Voltei.\nEstive ausente por " + endtime + "**",
        )
        AFK_.USERAFK_ON = {}
        AFK_.afk_time = None
        await asyncio.sleep(5)
        await shite.delete()
        AFK_.afk_on = False
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#AFKFALSE \n`Set AFK mode to False\n"
                + "Voltei.\nEstive ausente por "
                + endtime
                + "`",
            )


@catub.cat_cmd(
    incoming=True, func=lambda e: bool(e.mentioned or e.is_private), edited=False
)
async def on_afk(event):  # sourcery no-metrics
    if AFK_.afk_on is False:
        return
    afkmod = f"{random.choice(AFK1MOD)}"
    back_alivee = datetime.now()
    AFK_.afk_end = back_alivee.replace(microsecond=0)
    if AFK_.afk_star != {}:
        total_afk_time = AFK_.afk_end - AFK_.afk_star
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d, {h}h, {m}m, {s}s."
        elif h > 0:
            endtime += f"{h}h, {m}m, {s}s."
        else:
            endtime += f"{m}m, {s}s." if m > 0 else f"{s}s."
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text or "#afk" in current_message_text:
        return False
    if not await event.get_sender():
        return
    if AFK_.USERAFK_ON and not (await event.get_sender()).bot:
        msg = None
        if AFK_.afk_type == "media":
            if AFK_.reason:
                message_to_reply = (
                    f"**▸ Oi, estou ausente a {endtime}\n▸ Motivo :** __{AFK_.reason}__"
                )
            else:
                message_to_reply = f"__{afkmod}__"
            if event.chat_id:
                msg = await event.reply(message_to_reply, file=AFK_.media_afk.media)
        elif AFK_.afk_type == "text":
            if AFK_.msg_link and AFK_.reason:
                message_to_reply = (
                    f"**▸ Oi, estou ausente a {endtime}\n▸ Motivo :** __{AFK_.reason}__"
                )
            elif AFK_.reason:
                message_to_reply = (
                    f"**▸ Oi, estou ausente a {endtime}\n▸ Motivo :** __{AFK_.reason}__"
                )
            else:
                message_to_reply = f"__{afkmod}__"
            if event.chat_id:
                msg = await event.reply(message_to_reply)
        if event.chat_id in AFK_.last_afk_message:
            await AFK_.last_afk_message[event.chat_id].delete()
        AFK_.last_afk_message[event.chat_id] = msg
        if event.is_private:
            return
        hmm = await event.get_chat()
        if Config.PM_LOGGER_GROUP_ID == -100:
            return
        full = None
        try:
            full = await event.client.get_entity(event.message.from_id)
        except Exception as e:
            LOGS.info(str(e))
        messaget = media_type(event)
        resalt = f"#AFK_TAGS \n<b>Grupo : </b><code>{hmm.title}</code>"
        if full is not None:
            resalt += f"\n<b>De : </b> 👤{_format.htmlmentionuser(full.first_name , full.id)}"
        if messaget is not None:
            resalt += f"\n<b>Tipo de mensagem : </b><code>{messaget}</code>"
        else:
            resalt += f"\n<b>Mensagem : </b>{event.message.message}"
        resalt += f"\n<b>Link da mensagem : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>"
        if not event.is_private:
            await event.client.send_message(
                Config.PM_LOGGER_GROUP_ID,
                resalt,
                parse_mode="html",
                link_preview=False,
            )


@catub.cat_cmd(
    pattern="afk(?:\s|$)([\s\S]*)",
    command=("afk", plugin_category),
    info={
        "header": "Enables afk for your account",
        "description": "When you are in afk if any one tags you then your bot will reply as he is offline.\
        AFK mean away from keyboard.",
        "options": "If you want AFK reason with hyperlink use [ ; ] after reason, then paste the media link.",
        "usage": [
            "{tr}afk <reason>",
            "{tr}afk <reason> ; <link>",
        ],
        "examples": "{tr}afk Let Me Sleep",
        "note": "Switches off AFK when you type back anything, anywhere. You can use #afk in message to continue in afk without breaking it",
    },
)
async def _(event):
    "To mark yourself as afk i.e. Away from keyboard"
    AFK_.USERAFK_ON = {}
    AFK_.afk_time = None
    AFK_.last_afk_message = {}
    AFK_.afk_end = {}
    AFK_.afk_type = "text"
    start_1 = datetime.now()
    AFK_.afk_on = True
    AFK_.afk_star = start_1.replace(microsecond=0)
    if not AFK_.USERAFK_ON:
        input_str = event.pattern_match.group(1)
        if ";" in input_str:
            msg, mlink = input_str.split(";", 1)
            AFK_.reason = f"[{msg.strip()}]({mlink.strip()})"
            AFK_.msg_link = True
        else:
            AFK_.reason = input_str
            AFK_.msg_link = False
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            AFK_.afk_time = datetime.now()
        AFK_.USERAFK_ON = f"on: {AFK_.reason}"
        if AFK_.reason:
            await edit_delete(
                event, f"**Vou me ausentar. Motivo:** __{AFK_.reason}__", 5
            )
        else:
            await edit_delete(event, f"**Vou me ausentar.**", 5)
        if BOTLOG:
            if AFK_.reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFKTRUE \nSet AFK mode to True, and motivo is {AFK_.reason}",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#AFKTRUE \nSet AFK mode to True, and Reason is not mentioned",
                )


@catub.cat_cmd(
    pattern="mafk(?:\s|$)([\s\S]*)",
    command=("mafk", plugin_category),
    info={
        "header": "Enables afk for your account",
        "description": "When you are in afk if any one tags you then your bot will reply as he is offline.\
         AFK mean away from keyboard. Here it supports media unlike afk command",
        "options": "If you want AFK reason with hyperlink use [ ; ] after reason, then paste the media link.",
        "usage": [
            "{tr}mafk <reason> and reply to media",
        ],
        "examples": "{tr}mafk Let Me Sleep",
        "note": "Switches off AFK when you type back anything, anywhere. You can use #afk in message to continue in afk without breaking it",
    },
)
async def _(event):
    "To mark yourself as afk i.e. Away from keyboard (supports media)"
    reply = await event.get_reply_message()
    media_t = media_type(reply)
    if media_t == "Sticker" or not media_t:
        return await edit_or_reply(
            event, "`You haven't replied to any media to activate media afk`"
        )
    if not BOTLOG:
        return await edit_or_reply(
            event, "`To use media afk you need to set PRIVATE_GROUP_BOT_API_ID config`"
        )
    AFK_.USERAFK_ON = {}
    AFK_.afk_time = None
    AFK_.last_afk_message = {}
    AFK_.afk_end = {}
    AFK_.media_afk = None
    AFK_.afk_type = "media"
    start_1 = datetime.now()
    AFK_.afk_on = True
    AFK_.afk_star = start_1.replace(microsecond=0)
    if not AFK_.USERAFK_ON:
        input_str = event.pattern_match.group(1)
        AFK_.reason = input_str
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            AFK_.afk_time = datetime.now()
        AFK_.USERAFK_ON = f"on: {AFK_.reason}"
        if AFK_.reason:
            await edit_delete(
                event, f"**Vou me ausentar. Motivo:** __{AFK_.reason}__", 5
            )
        else:
            await edit_delete(event, f"**Vou me ausentar.**", 5)
        AFK_.media_afk = await reply.forward_to(BOTLOG_CHATID)
        if AFK_.reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#AFKTRUE \nSet AFK mode to True, and Motivo is {AFK_.reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#AFKTRUE \nSet AFK mode to True, and Reason is not mentioned",
            )
