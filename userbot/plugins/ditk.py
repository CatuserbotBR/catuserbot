#feelded

import io
import os
import re
import urllib
import shutil
from re import findall
import requests
from bs4 import BeautifulSoup
from telethon import events
from PIL import Image
from . import convert_toimage

ENABLE_HAREM = os.environ.get("ENABLE_HAREM", False)


opener = urllib.request.build_opener()
useragent = "Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36"
opener.addheaders = [("User-agent", useragent)]

@bot.on(admin_cmd(outgoing=True, pattern="waifu$"))
async def ParseSauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")
    results = {"similar_images": "", "best_guess": ""}
    try:
        for similar_image in soup.findAll("input", {"class": "gLFyf"}):
            url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
                similar_image.get("value")
            )
            results["similar_images"] = url
    except BaseException:
        pass
    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()
    return results

if ENABLE_HAREM:
    @bot.on(events.NewMessage(func=lambda x: x.sender_id == int(1733263647)))
    async def ihave3000waifu_uwantsome(event):
        if event.is_private:
            return
        if event.media:
            if 'Add' in event.raw_text:
                logger.info("OwO! A Waifu.")
                waifu_moment = io.BytesIO()
                waifu_dl_moment = await borg.download_media(event.media, waifu_moment)
                try:
                    image = Image.open(waifu_moment)
                except OSError:
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, "`A Waifu Appeared By Was Unable To Parse Image! Sorry :( \nError : OSError`")
                    return
                name = "waifu.png"
                image.save(name, "PNG")
                image.close()
                searchUrl = "https://www.google.com/searchbyimage/upload"
                file_img = {"encoded_image": (name, open(name, "rb")), "image_content": ""}
                response = requests.post(searchUrl, files=file_img, allow_redirects=False)
                os.remove(name)
                if response.status_code == 400:
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, "`A Waifu Appeared By Was Unable To Parse Image! Sorry :( \nError : Bad Status Code`")
                    return
                fetchUrl = response.headers["Location"]
                match = await ParseSauce(fetchUrl + "&preferences?hl=en&fg=1#languages")
                guessp = match["best_guess"]
                if not guessp:
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, "`A Waifu Appeared By Was Unable To Reverse Search Image! Sorry :(`")
                    return
                guess = guessp.replace("Results for", "").replace(" ", "")
                await borg.send_message(event.chat_id, f"/protecc {guess}")
                await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, f"**#Waifu_Moment** \n**Guessed Waifu :** `{guess}` \n**Chat ID :** `{event.chat_id}` \n**Powered By @feelded**")
