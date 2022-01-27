import os
from random import choice

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "extra"


@catub.cat_cmd(
    pattern="dist($)",
    command=("dist", plugin_category),
    info={
        "header": "Para distorcer a mídia respondida (sticker, vídeo e imagem)",
        "usage": [
            "{tr}dist <qualquer mídia>",
        ],
    },
)
async def _(event):
    "Distorts midia files"
    event.chat_id
    ded = await event.get_reply_message()
    mediatype = media_type(ded)
    await edit_or_reply(
        event,
        "`Distorcendo...`",
    )
    try:
        if mediatype in ["Gif", "Photo", "Video"]:
            await media(event, mediatype)
        elif mediatype in ["Audio"]:
            await audio(event)
        elif mediatype in ["Sticker", "Document"]:
            if ded.file.mime_type == "application/x-tgsticker":
                await tgs(event)
            elif mediatype in ["Sticker"]:
                await media(event, mediatype)
        else:
            await edit_or_reply(
                event,
                "**Você é burro?**",
            )
    except Exception as e:
        await edit_or_reply(event, str(e))
        return


# Here begins the end of world


async def tgs(message):
    "Destroys animated sticker"
    reply = await message.get_reply_message()
    await reply.download_media("tgs.tgs")
    os.system("lottie_convert.py tgs.tgs json.json")
    json = open("json.json", "r")
    jsn = json.read()
    json.close()
    jsn = (
        jsn.replace("[1]", "[20]")
        .replace("[2]", "[30]")
        .replace("[3]", "[40]")
        .replace("[4]", "[50]")
        .replace("[5]", "[60]")
    )

    open("json.json", "w").write(jsn)
    os.system("lottie_convert.py json.json tgs.tgs")
    await reply.reply(file="tgs.tgs")
    os.remove("json.json")
    os.remove("tgs.tgs")
    await message.delete()

async def media(event, mediatype):
    bot = "@distortionerbot"
    ded = await event.get_reply_message()
    chat = event.chat.id
    reply_to_id = await reply_id(event)
    async with event.client.conversation(bot, exclusive=False) as conv:  #
        try:
            start = await conv.send_message(ded)
            end = await conv.get_response()
            if media_type(end) in ["Sticker", "Photo"]:
                to_send = end
                await event.client.send_file(chat, file=to_send, reply_to=reply_to_id)
                await event.delete()
                await start.delete()
                await end.delete()
            else:
                end2 = await conv.get_response()
                to_send = end2
                await event.client.send_file(chat, file=to_send, reply_to=reply_to_id)
                await event.delete()
                await start.delete()
                await end.delete()
                await end2.delete()
        except YouBlockedUserError:
            await edit_delete(
                event, "**Erro:**\nDesbloqueie @distortionerbot e tente novamente."
            )


@catub.cat_cmd(
    pattern="dista( -r|$)",
    command=("dista", plugin_category),
    info={
        "header": "Distorce o áudio respondido.",
        "flags": {
            "r": "Use a flag `-r` para versão estourada",
        },
        "usage": ["{tr}dista", "{tr}dista -r"],
    },
)
async def kill_mp3(event):
    "Distorts audio files"
    flag = event.pattern_match.group(1)
    pawer = choice(range(10, 21))
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    try:
        if reply.file.mime_type != "audio/mpeg":
            await edit_delete(event, "`Responda a um áudio!`")
    except:
        await edit_delete(event, "`Responda a um áudio!`")

    await event.edit("`Baixando...`")
    if not os.path.isdir("destiny"):
        os.makedirs("destiny")
    else:
        os.system("rm -rf destiny")
        os.makedir("destiny")
    file = await reply.download_media("destiny/sed.mp3")
    ded_file = "destiny/ded-sed.opus"
    if flag == " -r":
        os.system(
            f'ffmpeg -i {file} -af "superequalizer=1b=20:2b=20:3b=20:4b=20:5b=20:6b=20:7b=20:8b=20:9b=20:10b=20:11b=20:12b=20:13b=20:14b=20:15b=20:16b=20:17b=20:18b=20,volume=5" {ded_file}'
        )
    else:
        os.system(f'ffmpeg -i {file} -filter_complex "vibrato=f={pawer}" {ded_file}')
    await event.edit("`Conversion done! Uploading audio.`")
    await event.client.send_file(
        event.chat_id,
        file=ded_file,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf destiny")
