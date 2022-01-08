import asyncio
import glob
import io
import os
import pathlib
import re
from datetime import datetime
from time import time

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import types
from telethon.utils import get_attributes
from wget import download
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from userbot import catub

from ..core import pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import progress, reply_id
from ..helpers.functions.utube import _mp3Dl, get_yt_video_id, get_ytthumb, ytsearch
from ..helpers.utils import _format
from . import hmention

BASE_YT_URL = "https://www.youtube.com/watch?v=" or "https://youtu.be/"
LOGS = logging.getLogger(__name__)
plugin_category = "misc"


video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        {"key": "FFmpegMetadata"},
    ],
    "outtmpl": "%(title)s.mp4",
    "logtostderr": False,
    "quiet": True,
}


async def ytdl_down(event, opts, url):
    ytdl_data = None
    try:
        await event.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{DE}`")
    except ContentTooShortError:
        await event.edit("`The download content was too short.`")
    except GeoRestrictedError:
        await event.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
    except MaxDownloadsReached:
        await event.edit("`Max-downloads limit has been reached.`")
    except PostProcessingError:
        await event.edit("`There was an error during post processing.`")
    except UnavailableVideoError:
        await event.edit("`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        await event.edit("`There was an error during info extraction.`")
    except Exception as e:
        await event.edit(f"**Error : **\n__{e}__")
    return ytdl_data


async def fix_attributes(
    path, info_dict: dict, supports_streaming: bool = False, round_message: bool = False
) -> list:
    """Avoid multiple instances of an attribute."""
    new_attributes = []
    video = False
    audio = False

    uploader = info_dict.get("uploader", "Unknown artist")
    duration = int(info_dict.get("duration", 0))
    suffix = path.suffix[1:]
    if supports_streaming and suffix != "mp4":
        supports_streaming = True

    attributes, mime_type = get_attributes(path)
    if suffix == "mp3":
        title = str(info_dict.get("title", info_dict.get("id", "Unknown title")))
        audio = types.DocumentAttributeAudio(
            duration=duration, voice=None, title=title, performer=uploader
        )
    elif suffix == "mp4":
        width = int(info_dict.get("width", 0))
        height = int(info_dict.get("height", 0))
        for attr in attributes:
            if isinstance(attr, types.DocumentAttributeVideo):
                duration = duration or attr.duration
                width = width or attr.w
                height = height or attr.h
                break
        video = types.DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=round_message,
            supports_streaming=supports_streaming,
        )

    if audio and isinstance(audio, types.DocumentAttributeAudio):
        new_attributes.append(audio)
    if video and isinstance(video, types.DocumentAttributeVideo):
        new_attributes.append(video)

    for attr in attributes:
        if (
            isinstance(attr, types.DocumentAttributeAudio)
            and not audio
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not video
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not isinstance(attr, types.DocumentAttributeVideo)
        ):
            new_attributes.append(attr)
    return new_attributes, mime_type


@catub.cat_cmd(
    pattern="yta(?:\s|$)([\s\S]*)",
    command=("yta", plugin_category),
    info={
        "header": "To download audio from many sites like Youtube",
        "description": "downloads the audio from the given link (Suports the all sites which support youtube-dl)",
        "examples": ["{tr}yta <reply to link>", "{tr}yta <link>"],
    },
)
async def download_audio(event):
    """To download audio from YouTube and many other sites."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await edit_or_reply(event, "`What I am Supposed to do? Give link`")
    catevent = await edit_or_reply(event, "`Preparing to download...`")
    reply_to_id = await reply_id(event)
    try:
        vid_data = YoutubeDL({"no-playlist": True}).extract_info(url, download=False)
    except ExtractorError:
        vid_data = {"title": url, "uploader": "Catuserbot", "formats": []}
    startTime = time()
    retcode = await _mp3Dl(url=url, starttime=startTime, uid="320")
    if retcode != 0:
        return await event.edit(str(retcode))
    _fpath = ""
    thumb_pic = None
    for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
        if _path.lower().endswith((".jpg", ".png", ".webp")):
            thumb_pic = _path
        else:
            _fpath = _path
    if not _fpath:
        return await edit_delete(catevent, "__Unable to upload file__")
    await catevent.edit(
        f"`Preparing to upload video:`\
        \n**{vid_data['title']}**\
        \nby *{vid_data['uploader']}*"
    )
    attributes, mime_type = get_attributes(str(_fpath))
    ul = io.open(pathlib.Path(_fpath), "rb")
    if thumb_pic is None:
        thumb_pic = str(
            await pool.run_in_thread(download)(await get_ytthumb(get_yt_video_id(url)))
        )
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(
                d,
                t,
                catevent,
                startTime,
                "trying to upload",
                file_name=os.path.basename(pathlib.Path(_fpath)),
            )
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        force_file=False,
        thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        caption=f"<b>File Name : </b><code>{vid_data.get('title', os.path.basename(pathlib.Path(_fpath)))}</code>",
        reply_to=reply_to_id,
        parse_mode="html",
    )
    for _path in [_fpath, thumb_pic]:
        os.remove(_path)
    await catevent.delete()


@catub.cat_cmd(
    pattern="ytv(?:\s|$)([\s\S]*)",
    command=("ytv", plugin_category),
    info={
        "header": "To download video from many sites like Youtube",
        "description": "downloads the video from the given link(Suports the all sites which support youtube-dl)",
        "examples": [
            "{tr}ytv <reply to link>",
            "{tr}ytv <link>",
        ],
    },
)
async def download_video(event):
    """To download video from YouTube and many other sites."""
    url = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not url and rmsg:
        myString = rmsg.text
        url = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
    if not url:
        return await edit_or_reply(event, "What I am Supposed to find? Give link")
    catevent = await edit_or_reply(event, "`Preparing to download...`")
    reply_to_id = await reply_id(event)
    ytdl_data = await ytdl_down(catevent, video_opts, url)
    if ytdl_down is None:
        return
    f = pathlib.Path(f"{ytdl_data['title']}.mp4".replace("|", "_"))
    catthumb = pathlib.Path(f"{ytdl_data['title']}.jpg".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = pathlib.Path(f"{ytdl_data['title']}.webp".replace("|", "_"))
    if not os.path.exists(catthumb):
        catthumb = None
    await catevent.edit(
        f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
    )
    ul = io.open(f, "rb")
    c_time = time()
    attributes, mime_type = await fix_attributes(f, ytdl_data, supports_streaming=True)
    uploaded = await event.client.fast_upload_file(
        file=ul,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, catevent, c_time, "upload", file_name=f)
        ),
    )
    ul.close()
    media = types.InputMediaUploadedDocument(
        file=uploaded,
        mime_type=mime_type,
        attributes=attributes,
        thumb=await event.client.upload_file(catthumb) if catthumb else None,
    )
    await event.client.send_file(
        event.chat_id,
        file=media,
        reply_to=reply_to_id,
        caption=ytdl_data["title"],
    )
    os.remove(f)
    if catthumb:
        os.remove(catthumb)
    await event.delete()

@catub.cat_cmd(
    pattern="insta ([\s\S]*)",
    command=("insta", plugin_category),
    info={
        "header": "Instagram post download ",
        "usage": [
            "{tr}insta <insta link>",
        ],
    },
)
async def _(event):
    "Insta Post Downloader"
    reply_to_id = await reply_id(event)
    link = event.pattern_match.group(1)
    if "www.instagram.com" not in link:
        await edit_or_reply(event, "` I need a Instagram link to download the post `")
        return
    chat = "@Void_IGDL_robot"
    async with event.client.conversation(chat) as conv:
        try:
            s = await conv.send_message(link)
            message = await conv.get_response()
            await event.edit(message.text)
            info = await conv.get_response()
            await event.client.send_file(
                event.chat_id,
                file=info,
                caption=f"• <a href={link}>Post Link</a> •",
                reply_to=reply_to_id,
                parse_mode="html",
            )
            await event.delete()
            await s.delete()
            await info.delete()
        except YouBlockedUserError:
            await edit_delete("`Unblock` **@Void_IGDL_robot** `and try again`")
