import asyncio
import base64
import io
import os
from pathlib import Path

from ShazamAPI import Shazam
from telethon import functions, types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from urlextract import URLExtract
from validators.url import url
from youtubesearchpython import Video

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import (
    deEmojify,
    hide_inlinebot,
    name_dl,
    song_dl,
    video_dl,
    yt_search,
)
from ..helpers.tools import media_type
from ..helpers.utils import _catutils, reply_id
from . import catub, hmention

plugin_category = "utils"
LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>Pesquisando...</code>"
SONG_NOT_FOUND = "<code>Desculpe! Não consegui encontrar nenhuma música</code>"
SONG_SENDING_STRING = "<code>Baixando...</code>"
SONGBOT_BLOCKED_STRING = "<code>Por favor, desbloqueie @songdl_bot e tente novamente</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@catub.cat_cmd(
    pattern="songg(320)?(?:\s|$)([\s\S]*)",
    command=("songg", plugin_category),
    info={
        "header": "Para obter músicas do youtube.",
        "description": "Basicamente este comando pesquisa no youtube e envia o primeiro vídeo como arquivo de áudio.",
        "flags": {
            "320": "se você usar song320, obterá qualidade de 320k, senão qualidade de 128k",
        },
        "usage": "{tr}songg <nome da música>",
        "examples": "{tr}songg mustang preto",
    },
)
async def _(event):
    "To search songs from youtube"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "`O que eu deveria encontrar?`")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "`Pesquisando...`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"Desculpe!. Não consigo encontrar nenhum vídeo/áudio relacionado para `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    stderr = (await _catutils.runcmd(song_cmd))[1]
    if stderr:
        return await catevent.edit(f"**Erro:** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**Erro:** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    catname = os.path.splitext(catname)[0]
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{catname}.mp3")
    if not os.path.exists(song_file):
        return await catevent.edit(
            f"Desculpe!. Não consigo encontrar nenhum vídeo/áudio relacionado para `{query}`"
        )
    await catevent.edit("`Baixando...`")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    ytdata = Video.get(video_link)
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"<b><i>➥ Título: {ytdata['title']}</i></b>\n<b><i>➥ Enviado por: {hmention}</i></b>",
        parse_mode="html",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@catub.cat_cmd(
    pattern="vsong(?:\s|$)([\s\S]*)",
    command=("vsong", plugin_category),
    info={
        "header": "Para obter músicas de vídeo do youtube.",
        "description": "Basicamente este comando pesquisa no youtube e envia o primeiro vídeo",
        "usage": "{tr}vsong <nome da música>",
        "examples": "{tr}vsong mustang preto",
    },
)
async def _(event):
    "To search video songs from youtube"
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "`O que eu deveria encontrar?`")
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    catevent = await edit_or_reply(event, "`Pesquisando...`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await catevent.edit(
            f"Desculpe!. Não consigo encontrar nenhum vídeo/áudio relacionado para `{query}`"
        )
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    video_cmd = video_dl.format(video_link=video_link)
    stderr = (await _catutils.runcmd(video_cmd))[1]
    if stderr:
        return await catevent.edit(f"**Erro:** `{stderr}`")
    catname, stderr = (await _catutils.runcmd(name_cmd))[:2]
    if stderr:
        return await catevent.edit(f"**Erro:** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    # if stderr:
    #    return await catevent.edit(f"**Error :** `{stderr}`")
    catname = os.path.splitext(catname)[0]
    vsong_file = Path(f"{catname}.mp4")
    if not os.path.exists(vsong_file):
        vsong_file = Path(f"{catname}.mkv")
    elif not os.path.exists(vsong_file):
        return await catevent.edit(
            f"Desculpe!. Não consigo encontrar nenhum vídeo/áudio relacionado para `{query}`"
        )
    await catevent.edit("`Baixando...`")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    ytdata = Video.get(video_link)
    await event.client.send_file(
        event.chat_id,
        vsong_file,
        force_document=False,
        caption=f"<b><i>➥ Título: {ytdata['title']}</i></b>\n<b><i>➥ Enviado por: {hmention}</i></b>",
        parse_mode="html",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await catevent.delete()
    for files in (catthumb, vsong_file):
        if files and os.path.exists(files):
            os.remove(files)


@catub.cat_cmd(
    pattern="wsong$",
    command=("wsong", plugin_category),
    info={
        "header": "Para fazer uma pesquisa reversa de uma música.",
        "description": "Pesquisa reversa de música usando shazam api",
        "usage": "{tr}wsong <resposta para voz/audio>",
    },
)
async def shazamcmd(event):
    "To reverse search song."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "__Responda ao clipe de voz ou clipe de áudio para pesquisar essa música de forma inversa.__"
        )
    catevent = await edit_or_reply(event, "__Baixando o clipe de áudio...__")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(catevent, f"**Não foi possível encontrar nenhuma música.**")

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**➥ Música:** `{song}`", reply_to=reply
    )
    await catevent.delete()


@catub.cat_cmd(
    pattern="song(?:\s|$)([\s\S]*)",
    command=("song", plugin_category),
    info={
        "header": "Para pesquisar músicas e enviar para o telegram",
        "description": "Pesquisa a música que você digitou na consulta e envia a qualidade dela é 320k",
        "usage": "{tr}song <nome da música>",
        "examples": "{tr}song mustang preto",
    },
)
async def _(event):
    "To search songs by bot"
    song = event.pattern_match.group(1)
    chat = "@songdl_bot"
    reply_id_ = await reply_id(event)
    catevent = await edit_or_reply(event, SONG_SEARCH_STRING, parse_mode="html")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(song)
            hmm = await conv.get_response()
            while hmm.edit_hide is not True:
                await asyncio.sleep(0.1)
                hmm = await event.client.get_messages(chat, ids=hmm.id)
            baka = await event.client.get_messages(chat)
            if baka[0].message.startswith(
                ("I don't like to say this but I failed to find any such song.")
            ):
                await delete_messages(event, chat, purgeflag)
                return await edit_delete(
                    catevent, SONG_NOT_FOUND, parse_mode="html", time=5
                )
            await catevent.edit(SONG_SENDING_STRING, parse_mode="html")
            await baka[0].click(0)
            await conv.get_response()
            await conv.get_response()
            music = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await catevent.edit(SONGBOT_BLOCKED_STRING, parse_mode="html")
        await event.client.send_file(
            event.chat_id,
            music,
            caption=f"<b>➥ Música: <code>{song}</code></b>",
            parse_mode="html",
            reply_to=reply_id_,
        )
        await catevent.delete()
        await delete_messages(event, chat, purgeflag)


@catub.cat_cmd(
    pattern="szm$",
    command=("szm", plugin_category),
    info={
        "header": "Para fazer a pesquisa de um áudio.",
        "description": "o comprimento do arquivo de música deve ser em torno de 10 segundos, então use o plugin ffmpeg para cortá-lo.",
        "usage": "{tr}szm",
    },
)
async def _(event):
    "To reverse search music by bot."
    if not event.reply_to_msg_id:
        return await edit_delete(event, "```Responda a uma mensagem de áudio.```")
    reply_message = await event.get_reply_message()
    chat = "@auddbot"
    catevent = await edit_or_reply(event, "```Identificando a música```")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(reply_message)
            check = await conv.get_response()
            if not check.text.startswith("Audio received"):
                return await catevent.edit(
                    "Um erro ao identificar a música. Tente usar uma mensagem de áudio de 5 a 10 segundos."
                )
            await catevent.edit("Wait just a sec...")
            result = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await catevent.edit("```Por favor, desbloqueie (@auddbot) e tente novamente```")
            return
    namem = f"**Nome da música:**`{result.text.splitlines()[0]}`\
        \n\n**Detalhes: **__{result.text.splitlines()[2]}__"
    await catevent.edit(namem)


@catub.cat_cmd(
    pattern="dzd ?(.*)",
    command=("dzd", plugin_category),
    info={
        "header": "Para baixar músicas via bot DeezLoad",
        "description": "Downloader Spotify/Deezer ",
        "usage": "{tr}dzd <link da música>",
        "examples": "{tr}dzd https://www.deezer.com/track/3657911",
    },
)
async def dzd(event):
    "To download song via Deezload2bot"
    link = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    pro = link or reply_message.text
    extractor = URLExtract()
    plink = extractor.find_urls(pro)
    reply_to_id = await reply_id(event)
    if not link and not reply_message:
        catevent = await edit_delete(
            event, "**Preciso de um link para baixar, gênio. (._.)**"
        )
    else:
        catevent = await edit_or_reply(event, "**Baixando...!**")
    chat = "@deezload2bot"
    async with event.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(plink)
            details = await conv.get_response()
            song = await conv.get_response()
            """ - don't spam notif - """
            await event.client.send_read_acknowledge(conv.chat_id)
            await catevent.delete()
            await event.client.send_file(
                event.chat_id, song, caption=details.text, reply_to=reply_to_id
            )
            await event.client.delete_messages(
                conv.chat_id, [msg.id, details.id, song.id]
            )
        except YouBlockedUserError:
            await catevent.edit("**Erro:** `desbloqueie` @deezload2bot `e tente novamente!`")
            return


@catub.cat_cmd(
    pattern="sdl",
    command=("sdl", plugin_category),
    info={
        "header": "Spotify/Deezer Downloader",
        "usage": [
            "{tr}sdl <song link>",
            "{tr}sdl <resposta para Spotify/Deezer link>",
        ],
    },
)
async def wave(odi):
    "Song Downloader via Bot"
    song = "".join(odi.text.split(maxsplit=1)[1:])
    songr = await odi.get_reply_message()
    reply_to_id = await reply_id(odi)
    link = song or songr.text
    if not link:
        await edit_delete(odi, "`Me dê um link de música`")
    elif not link:
        await edit_delete(odi, "`Me dê um link de música`")
    elif ".com" not in link:
        await edit_delete(odi, "`Me dê um link de música`")
    else:
        await odi.edit("`Baixando...`")
        chat = "@DeezerMusicBot"
        async with odi.client.conversation(chat) as conv:
            try:
                await odi.client(functions.contacts.UnblockRequest(conv.chat_id))
                start = await conv.send_message("/start")
                await conv.get_response()
                end = await conv.send_message(link)
                music = await conv.get_response()
                if not music.audio:
                    await odi.edit(f"`Nenhum resultado encontrado para {song}`")
                else:
                    result = await odi.client.send_file(
                        odi.chat_id, music, reply_to=reply_to_id, caption=False
                    )
                    await odi.delete()
                msgs = []
                for _ in range(start.id, end.id + 2):
                    msgs.append(_)
                await odi.client.delete_messages(conv.chat_id, msgs)
                await odi.client.send_read_acknowledge(conv.chat_id)
            except result:
                await odi.reply("`Algo deu errado`")


@catub.cat_cmd(
    pattern="mev ?(.*)",
    command=("mev", plugin_category),
    info={
        "header": "Pesquisa e envia a voz do meme.",
        "usage": "{tr}mev <meme>",
        "examples": "{tr}mev Hello motherfucker",
    },
)
async def nope(event):
    "Meme voice by bot"
    mafia = event.pattern_match.group(1)
    lol = deEmojify(mafia)
    bot = "@myinstantsbot"
    reply_to_id = await reply_id(event)
    if not lol:
        if event.is_reply:
            lol = (await event.get_reply_message()).message
        else:
            lol = "bruh"
    await hide_inlinebot(event.client, bot, lol, event.chat_id, reply_to_id)
    await event.delete()


@catub.cat_cmd(
    pattern="ssong ?(.*)",
    command=("ssong", plugin_category),
    info={
        "header": "Ele enviará o link do Spotify/Deezer da sua pesquisa.",
        "flags": {"-d": "Para Link do Deezer"},
        "usage": [
            "{tr}ssong <nome da música>",
            "{tr}ssong <resposta>",
            "{tr}ssong -d <nome da música>",
            "{tr}ssong -d <resposta>",
        ],
    },
)
async def music(event):
    "Generate Spotify/Deezer link from song names"
    if event.fwd_from:
        return
    music = None
    argument = event.pattern_match.group(1)
    await edit_or_reply(event, "`Enviando o link da música, espere...`")
    try:
        flag = event.pattern_match.group(1).split()[0]
    except IndexError:
        flag = ""

    if "-d" in flag:
        music = event.pattern_match.group(1)[3:]
        if not music and event.reply_to_msg_id:
            music = (await event.get_reply_message()).text or None
    elif argument:
        music = argument
    elif event.reply_to_msg_id:
        music = (await event.get_reply_message()).text or None

    if not music:
        return await edit_delete(event, "`Coloque uma música`")

    bot = "@deezload2bot" if "-d" in flag else "@songdl_bot"
    sike = "Deezer" if "-d" in flag else "Spotify"
    reply_to_id = await reply_id(event)
    run = await event.client.inline_query(bot, music)

    try:
        result = await run[0].click("me")
        await result.delete()
    except IndexError:
        await edit_delete(event, "`Bruh")
        return

    if not (result.text).startswith("https://"):
        await event.client.send_message(
            event.chat_id,
            f"**✘ Nome:** __{music}__\n**✘ Site:** __{sike}__\n**✘ Link:** __OCORREU ALGUM ERRO__",
            reply_to=reply_to_id,
        )
    else:
        await event.client.send_message(
            event.chat_id,
            f"**✘ Nome:** __{music.title()}__\n**✘ Site:** __{sike}__\n**✘ Link:** __{result.text}__",
            link_preview=True,
            reply_to=reply_to_id,
        )

    await event.delete()
