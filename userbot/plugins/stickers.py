import asyncio
import base64
import io
import math
import os
import random
import re
import string
import urllib.request

import cloudscraper
import emoji as catemoji
from bs4 import BeautifulSoup as bs
from PIL import Image
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import animator, crop_and_divide
from ..helpers.tools import media_type
from ..helpers.utils import _cattools
from ..sql_helper.globals import gvarstatus

plugin_category = "fun"


combot_stickers_url = "https://combot.org/telegram/stickers?q="

EMOJI_SEN = [
    "Можно отправить несколько смайлов в одном сообщении, однако мы рекомендуем использовать не больше одного или двух на каждый стикер.",
    "You can list several emoji in one message, but I recommend using no more than two per sticker",
    "Du kannst auch mehrere Emoji eingeben, ich empfehle dir aber nicht mehr als zwei pro Sticker zu benutzen.",
    "Você pode listar vários emojis em uma mensagem, mas recomendo não usar mais do que dois por cada sticker.",
    "Puoi elencare diverse emoji in un singolo messaggio, ma ti consiglio di non usarne più di due per sticker.",
    "emoji",
]

KANGING_STR = [
    "Usando magia para roubar essa figurinha...",
    "Roubando sua figurinha hehe...",
    "Convidando essa figurinha para meu pack...",
    "Roubando essa figurinha...",
    "Figurinha legal essa, hein?!\nSe importa se eu roubar ela?!..",
    "Eu roubei sua figurinha\nhehe.",
    "Ei olhe pra lá (☉｡☉)!→\nEnquanto eu estou roubando isso...",
    "Aprisionando essa figurinha...",
    "O Sr.Ladrão está roubando essa figurinha...",
    "Plagiando hehe...",
    "Ai carinha que mora logo ali, me passa uma figurinha...",
]


def verify_cond(catarray, text):
    return any(i in text for i in catarray)


def pack_name(userid, pack, is_anim, is_video):
    if is_anim:
        return f"catuserbot_{userid}_{pack}_anim"
    elif is_video:
        return f"catuserbot_{userid}_{pack}_vid"
    return f"catuserbot_{userid}_{pack}"


def char_is_emoji(character):
    return character in catemoji.UNICODE_EMOJI["en"]


def pack_nick(username, pack, is_anim, is_video):
    if gvarstatus("CUSTOM_STICKER_PACKNAME"):
        if is_anim:
            return f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack} (Animated)"
        elif is_video:
            return f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol. {pack} (Video)"
        return f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} Vol.{pack}"

    if is_anim:
        return f"@{username} Vol.{pack} (Animated)"
    elif is_video:
        return f"@{username} Vol. {pack} (Video)"
    else:
        return f"@{username} Vol.{pack}"


async def delpack(catevent, conv, cmd, args, packname):
    try:
        await conv.send_message(cmd)
    except YouBlockedUserError:
        await catevent.edit("Você bloqueou o bot @stickers , desbloqueie e tente.")
        return None, None
    await conv.send_message("/delpack")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("Sim, eu tenho certeza absoluta")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)


async def resize_photo(photo):
    """Redimensione a foto fornecida para 512x512"""
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


async def newpacksticker(
    catevent,
    conv,
    cmd,
    args,
    pack,
    packnick,
    is_video,
    emoji,
    packname,
    is_anim,
    stfile,
    otherpack=False,
    pkang=False,
):
    try:
        await conv.send_message(cmd)
    except YouBlockedUserError:
        await catevent.edit("Você bloqueou o bot @stickers , desbloqueie e tente.")
        if not pkang:
            return None, None, None
        return None, None
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packnick)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if is_video:
        await conv.send_file("animate.webm")
    elif is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        os.remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await catevent.edit(
            f"Falha ao adicionar a figurinha, use o bot @Stickers para adicionar a figurinha manualmente.\n**error :**{rsp}"
        )
        if not pkang:
            return None, None, None
        return None, None
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/publish")
    if is_anim:
        await conv.get_response()
        await conv.send_message(f"<{packnick}>")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("/skip")
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message(packname)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return otherpack, packname, emoji
    return pack, packname


async def add_to_pack(
    catevent,
    conv,
    args,
    packname,
    pack,
    userid,
    username,
    is_video,
    is_anim,
    stfile,
    emoji,
    cmd,
    pkang=False,
):
    try:
        await conv.send_message("/addsticker")
    except YouBlockedUserError:
        await catevent.edit("Você bloqueou o bot @stickers , desbloqueie e tente.")
        if not pkang:
            return None, None
        return None, None
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    x = await conv.get_response()
    while ("50" in x.text) or ("120" in x.text):
        try:
            val = int(pack)
            pack = val + 1
        except ValueError:
            pack = 1
        packname = pack_name(userid, pack, is_anim, is_video)
        packnick = pack_nick(username, pack, is_anim, is_video)
        await catevent.edit(f"`Mudando para o Pack {pack} devido a espaço insuficiente`")
        await conv.send_message(packname)
        x = await conv.get_response()
        if x.text == "pack inválido selecionado.":
            return await newpacksticker(
                catevent,
                conv,
                cmd,
                args,
                pack,
                packnick,
                is_video,
                emoji,
                packname,
                is_anim,
                stfile,
                otherpack=True,
                pkang=pkang,
            )
    if is_video:
        await conv.send_file("animate.webm")
        os.remove("animate.webm")
    elif is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        os.remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await catevent.edit(
            f"Falha ao adicionar a figurinha, use o bot @Stickers para adicionar a figurinha manualmente.\n**error :**{rsp}"
        )
        if not pkang:
            return None, None
        return None, None
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/done")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return packname, emoji
    return pack, packname


@catub.cat_cmd(
    pattern="kang(?:\s|$)([\s\S]*)",
    command=("kang", plugin_category),
    info={
        "header": "Para roubar uma figurinha.",
        "description": "Roube o arquivo de figurinha/imagem/vídeo/gif/webm para o pack especificado e usa o(s) emoji(s) que você escolheu",
        "usage": "{tr}kang [emoji('s)] [numero]",
    },
)
async def kang(args):  # sourcery no-metrics
    "Para roubar uma figurinha."
    photo = None
    emojibypass = False
    is_anim = False
    is_video = False
    emoji = None
    message = await args.get_reply_message()
    user = await args.client.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"cat_{user.id}"
    else:
        username = user.username
    userid = user.id
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await args.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await args.client.download_media(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
            await args.client.download_media(
                message.media.document, "AnimatedSticker.tgs"
            )
            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        elif message.media.document.mime_type in ["video/mp4", "video/webm"]:
            if message.media.document.mime_type == "video/webm":
                catevent = await edit_or_reply(args, f"`{random.choice(KANGING_STR)}`")
                sticker = await args.client.download_media(
                    message.media.document, "animate.webm"
                )
            else:
                catevent = await edit_or_reply(args, "__Baixando...__")
                sticker = await animator(message, args, catevent)
                await edit_or_reply(catevent, f"`{random.choice(KANGING_STR)}`")
            is_video = True
            emoji = "😂"
            emojibypass = True
            photo = 1
        else:
            await edit_delete(args, "`Arquivo não suportado!`")
            return
    else:
        await edit_delete(args, "`Eu não posso roubar isso...`")
        return
    if photo:
        splat = ("".join(args.text.split(maxsplit=1)[1:])).split()
        emoji = emoji if emojibypass else "😂"
        pack = 1
        if len(splat) == 2:
            if char_is_emoji(splat[0][0]):
                if char_is_emoji(splat[1][0]):
                    return await catevent.edit("Verifique `.info stickers`")
                pack = splat[1]  # User sent both
                emoji = splat[0]
            elif char_is_emoji(splat[1][0]):
                pack = splat[0]  # User sent both
                emoji = splat[1]
            else:
                return await catevent.edit("Verifique `.info stickers`")
        elif len(splat) == 1:
            if char_is_emoji(splat[0][0]):
                emoji = splat[0]
            else:
                pack = splat[0]
        packname = pack_name(userid, pack, is_anim, is_video)
        packnick = pack_nick(username, pack, is_anim, is_video)
        cmd = "/newpack"
        stfile = io.BytesIO()
        if is_video:
            cmd = "/newvideo"
        elif is_anim:
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            stfile.name = "sticker.png"
            image.save(stfile, "PNG")
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with args.client.conversation("@Stickers") as conv:
                packname, emoji = await add_to_pack(
                    catevent,
                    conv,
                    args,
                    packname,
                    pack,
                    userid,
                    username,
                    is_video,
                    is_anim,
                    stfile,
                    emoji,
                    cmd,
                )
            if packname is None:
                return
            await edit_delete(
                catevent,
                f"`Figurinha roubada com sucesso!\
                    \nSeu pack está` [aqui](t.me/addstickers/{packname}) `e o emoji para a figurinha roubada é {emoji}`",
                parse_mode="md",
                time=10,
            )
        else:
            await catevent.edit("`Preparando um novo pack...`")
            async with args.client.conversation("@Stickers") as conv:
                otherpack, packname, emoji = await newpacksticker(
                    catevent,
                    conv,
                    cmd,
                    args,
                    pack,
                    packnick,
                    is_video,
                    emoji,
                    packname,
                    is_anim,
                    stfile,
                )
            if os.path.exists(sticker):
                os.remove(sticker)
            if otherpack is None:
                return
            if otherpack:
                await edit_delete(
                    catevent,
                    f"`Figurinha roubada para um pack diferente !\
                    \nE o pack recém-criado está` [aqui](t.me/addstickers/{packname}) `e o emoji para a figurinha roubada é {emoji}`",
                    parse_mode="md",
                    time=10,
                )
            else:
                await edit_delete(
                    catevent,
                    f"`Figurinha roubada com sucesso!\
                    \nSeu pack esta` [aqui](t.me/addstickers/{packname}) `e o emoji para a figurinha roubada é {emoji}`",
                    parse_mode="md",
                    time=10,
                )


@catub.cat_cmd(
    pattern="pkang(?:\s|$)([\s\S]*)",
    command=("pkang", plugin_category),
    info={
        "header": "Para roubar o pack de figurinha inteiro.",
        "description": "Roube todo o pack de figurinhas da figurinha respondida para o pack especificado",
        "usage": "{tr}pkang [número]",
    },
)
async def pack_kang(event):  # sourcery no-metrics
    "Para roubar o pack de figurinha inteiro."
    user = await event.client.get_me()
    if user.username:
        username = user.username
    else:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"cat_{user.id}"
    photo = None
    userid = user.id
    is_anim = False
    is_video = False
    emoji = None
    reply = await event.get_reply_message()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply or media_type(reply) is None or media_type(reply) != "Sticker":
        return await edit_delete(
            event, "`Responda a qualquer figurinha para enviar todas as figurinhas desse pack`"
        )
    try:
        stickerset_attr = reply.document.attributes[1]
        catevent = await edit_or_reply(
            event, "`Buscando detalhes do pack de figurinhas, aguarde..`"
        )
    except BaseException:
        return await edit_delete(
            event, "`Isso não é uma figurinha. Responda a uma figurinha.`", 5
        )
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await edit_delete(
            catevent,
            "`Acho que essa figurinha não faz parte de nenhum pack. Então, eu não posso roubar este pack de figurinhas, tente roubar uma figurinha em um pack`",
        )
    kangst = 1
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    noofst = get_stickerset.set.count
    blablapacks = []
    blablapacknames = []
    pack = None
    for message in reqd_sticker_set.documents:
        if "image" in message.mime_type.split("/"):
            await edit_or_reply(
                catevent,
                f"`Este pack de figurinhas está sendo roubado agora. Status do processo do roubo : {kangst}/{noofst}`",
            )
            photo = io.BytesIO()
            await event.client.download_media(message, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.attributes
            ):
                emoji = message.attributes[1].alt
        elif "tgsticker" in message.mime_type:
            await edit_or_reply(
                catevent,
                f"`Este pack de figurinhas está sendo roubado agora. Status do processo do roubo : {kangst}/{noofst}`",
            )
            await event.client.download_media(message, "AnimatedSticker.tgs")
            attributes = message.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            is_anim = True
            photo = 1
        else:
            await edit_delete(catevent, "`Arquivo não suportado!`")
            return
        if photo:
            splat = ("".join(event.text.split(maxsplit=1)[1:])).split()
            emoji = emoji or "😂"
            if pack is None:
                pack = 1
                if len(splat) == 1:
                    pack = splat[0]
                elif len(splat) > 1:
                    return await edit_delete(
                        catevent,
                        "`Desculpe, o nome dado não pode ser usado para o pack ou não há pack com esse nome`",
                    )
            try:
                cat = Get(cat)
                await event.client(cat)
            except BaseException:
                pass
            packnick = pack_nick(username, pack, is_anim, is_video)
            packname = pack_name(userid, pack, is_anim, is_video)
            cmd = "/newpack"
            stfile = io.BytesIO()
            if is_anim:
                cmd = "/newanimated"
            else:
                image = await resize_photo(photo)
                stfile.name = "sticker.png"
                image.save(stfile, "PNG")
            response = urllib.request.urlopen(
                urllib.request.Request(f"http://t.me/addstickers/{packname}")
            )
            htmlstr = response.read().decode("utf8").split("\n")
            if (
                "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
                in htmlstr
            ):
                async with event.client.conversation("@Stickers") as conv:
                    pack, catpackname = await newpacksticker(
                        catevent,
                        conv,
                        cmd,
                        event,
                        pack,
                        packnick,
                        is_video,
                        emoji,
                        packname,
                        is_anim,
                        stfile,
                        pkang=True,
                    )
            else:
                async with event.client.conversation("@Stickers") as conv:
                    pack, catpackname = await add_to_pack(
                        catevent,
                        conv,
                        event,
                        packname,
                        pack,
                        userid,
                        username,
                        is_video,
                        is_anim,
                        stfile,
                        emoji,
                        cmd,
                        pkang=True,
                    )
            if catpackname is None:
                return
            if catpackname not in blablapacks:
                blablapacks.append(catpackname)
                blablapacknames.append(pack)
        kangst += 1
        await asyncio.sleep(2)
    result = "`Este pack de figurinhas foi roubado para o seguinte pack:`\n"
    for i in enumerate(blablapacks):
        result += (
            f"  •  [pack {blablapacknames[i[0]]}](t.me/addstickers/{blablapacks[i[0]]})"
        )
    await catevent.edit(result)


@catub.cat_cmd(
    pattern="vas$",
    command=("vas", plugin_category),
    info={
        "header": "Converte vídeo/gif em figurinha animado",
        "description": "Converte vídeo/gif para arquivo .webm e envia um figurinha animado temporário desse arquivo",
        "usage": "{tr}vas <responda a um Video/Gif>",
    },
)
async def pussycat(args):
    "Para roubar uma figurinha."  # scam :('  Dom't kamg :/@Jisan7509
    message = await args.get_reply_message()
    user = await args.client.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            user.first_name
        except UnicodeDecodeError:
            f"cat_{user.id}"
    else:
        user.username
    userid = user.id
    if message and message.media:
        if "video/mp4" in message.media.document.mime_type:
            catevent = await edit_or_reply(args, "__ Baixando...__")
            sticker = await animator(message, args, catevent)
            await edit_or_reply(catevent, f"`{random.choice(KANGING_STR)}`")
        else:
            await edit_delete(args, "`Responda a um video/gif...!`")
            return
    else:
        await edit_delete(args, "`Eu não posso converter isso...`")
        return
    cmd = "/newvideo"
    packname = f"Catub_{userid}_temp_pack"
    response = urllib.request.urlopen(
        urllib.request.Request(f"http://t.me/addstickers/{packname}")
    )
    htmlstr = response.read().decode("utf8").split("\n")
    if (
        "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
        not in htmlstr
    ):
        async with args.client.conversation("@Stickers") as xconv:
            await delpack(
                catevent,
                xconv,
                cmd,
                args,
                packname,
            )
    await catevent.edit("`Espere, fazendo a figurinha...`")
    async with args.client.conversation("@Stickers") as conv:
        otherpack, packname, emoji = await newpacksticker(
            catevent,
            conv,
            "/newvideo",
            args,
            1,
            "Catub",
            True,
            "😂",
            packname,
            False,
            io.BytesIO(),
        )
    if otherpack is None:
        return
    await catevent.delete()
    await args.client.send_file(
        args.chat_id,
        sticker,
        force_document=True,
        caption=f"**[Pre-visualização da figurinha](t.me/addstickers/{packname})**\n*__Ele será removido automaticamente na sua próxima conversão.__",
        reply_to=message,
    )
    if os.path.exists(sticker):
        os.remove(sticker)


@catub.cat_cmd(
    pattern="gridpack(?:\s|$)([\s\S]*)",
    command=("gridpack", plugin_category),
    info={
        "header": "Para dividir a imagem respondida e criar um pack de figurinhas.",
        "flags": {
            "-e": "para usar emoji personalizado por padrão o emoji é ▫️ .",
        },
        "usage": [
            "{tr}gridpack <packname>",
            "{tr}gridpack -e👌 <packname>",
        ],
        "examples": [
            "{tr}gridpack -e👌 CatUserbot",
        ],
    },
)
async def pic2packcmd(event):
    "Para dividir a imagem respondida e criar um pack de figurinhas."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Photo", "Sticker"]:
        return await edit_delete(event, "__Responda à foto ou figurinha para fazer o pack.__")
    if mediatype == "Sticker" and reply.document.mime_type == "application/x-tgsticker":
        return await edit_delete(
            event,
            "__Responda à foto ou figurinha para fazer o pack. A figurinha animado não é compatível__",
        )
    args = event.pattern_match.group(1)
    if not args:
        return await edit_delete(
            event, "__Qual é o seu nome de pack?. passar junto com cmd.__"
        )
    catevent = await edit_or_reply(event, "__Cortando e ajustando a imagem...__")
    try:
        emoji = (re.findall(r"-e[\U00010000-\U0010ffff]+", args))[0]
        args = args.replace(emoji, "")
        emoji = emoji.replace("-e", "")
    except Exception:
        emoji = "▫️"
    chat = "@Stickers"
    name = "CatUserbot_" + "".join(
        random.choice(list(string.ascii_lowercase + string.ascii_uppercase))
        for _ in range(16)
    )
    image = await _cattools.media_to_pic(catevent, reply, noedits=True)
    if image[1] is None:
        return await edit_delete(
            image[0], "__Não foi possível extrair a imagem da mensagem respondida.__"
        )
    image = Image.open(image[1])
    w, h = image.size
    www = max(w, h)
    img = Image.new("RGBA", (www, www), (0, 0, 0, 0))
    img.paste(image, ((www - w) // 2, 0))
    newimg = img.resize((100, 100))
    new_img = io.BytesIO()
    new_img.name = name + ".png"
    images = await crop_and_divide(img)
    newimg.save(new_img)
    new_img.seek(0)
    catevent = await event.edit("__Fazendo o pack.__")
    async with event.client.conversation(chat) as conv:
        i = 0
        try:
            await event.client.send_message(chat, "/cancel")
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            await event.client.send_message(chat, "/newpack")
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            await event.client.send_message(chat, args)
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            for im in images:
                img = io.BytesIO(im)
                img.name = name + ".png"
                img.seek(0)
                await event.client.send_file(chat, img, force_document=True)
                await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
                await event.client.send_message(chat, emoji)
                await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
                await event.client.send_read_acknowledge(conv.chat_id)
                await asyncio.sleep(1)
                i += 1
                await catevent.edit(
                    f"__Fazendo o pack.\nProgresso: {i}/{len(images)}__"
                )
            await event.client.send_message(chat, "/publish")
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            await event.client.send_file(chat, new_img, force_document=True)
            await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
            await event.client.send_message(chat, name)
            ending = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=chat)
            )
            await event.client.send_read_acknowledge(conv.chat_id)
            for packname in ending.raw_text.split():
                stick_pack_name = packname
                if stick_pack_name.startswith("https://t.me/"):
                    break
            await catevent.edit(
                f"__criou com sucesso o pack para a mídia respondida : __[{args}]({stick_pack_name})"
            )

        except YouBlockedUserError:
            await catevent.edit(
                "__Você bloqueou o bot @Stickers. desbloqueie e tente novamente__"
            )


@catub.cat_cmd(
    pattern="stkrinfo$",
    command=("stkrinfo", plugin_category),
    info={
        "header": "Para obter informações sobre uma figurinha.",
        "description": "Obtém informações sobre o pack de figurinhas",
        "usage": "{tr}stkrinfo",
    },
)
async def get_pack_info(event):
    "Para obter informações sobre uma figurinha de escolha."
    if not event.is_reply:
        return await edit_delete(
            event, "`Não consigo buscar informações do nada, posso?!`", 5
        )
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await edit_delete(
            event, "`Responda a uma figurinha para obter os detalhes do pack`", 5
        )
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        catevent = await edit_or_reply(
            event, "`Buscando detalhes do pack de figurinhas, aguarde..`"
        )
    except BaseException:
        return await edit_delete(
            event, "`Isso não é uma figurinha. Responda a uma figurinha.`", 5
        )
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await catevent.edit("`Isso não é uma figurinha. Responda a uma figurinha.`")
    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = (
        f"**Titulo da figurinha:** `{get_stickerset.set.title}\n`"
        f"**Nome Curto da figurinha:** `{get_stickerset.set.short_name}`\n"
        f"**Oficial:** `{get_stickerset.set.official}`\n"
        f"**Arquivado:** `{get_stickerset.set.archived}`\n"
        f"**figurinhas no Pack:** `{get_stickerset.set.count}`\n"
        f"**Emojis no Pack:**\n{' '.join(pack_emojis)}"
    )
    await catevent.edit(OUTPUT)


@catub.cat_cmd(
    pattern="stickers ?([\s\S]*)",
    command=("stickers", plugin_category),
    info={
        "header": "Para obter a lista de packs de figurinhas com nome próprio.",
        "description": "mostra a lista de packs de figurinhas não animados com esse nome.",
        "usage": "{tr}stickers <pesquisa>",
    },
)
async def cb_sticker(event):
    "Para obter a lista de packs de figurinhas com nome próprio."
    split = event.pattern_match.group(1)
    if not split:
        return await edit_delete(event, "`Forneça algum nome para procurar o pack.`", 5)
    catevent = await edit_or_reply(event, "`Pesquisando packs de figurinhas....`")
    scraper = cloudscraper.create_scraper()
    text = scraper.get(combot_stickers_url + split).text
    soup = bs(text, "lxml")
    results = soup.find_all("div", {"class": "sticker-pack__header"})
    if not results:
        return await edit_delete(catevent, "`No results found :(.`", 5)
    reply = f"**Os packs de figurinhas encontradas para {split} são :**"
    for pack in results:
        if pack.button:
            packtitle = (pack.find("div", "sticker-pack__title")).get_text()
            packlink = (pack.a).get("href")
            packid = (pack.button).get("data-popup")
            reply += f"\n **• ID: **`{packid}`\n [{packtitle}]({packlink})"
    await catevent.edit(reply)
