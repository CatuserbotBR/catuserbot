import json
import re

from bs4 import BeautifulSoup
from requests import get

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="magisk$",
    command=("magisk", plugin_category),
    info={
        "header": "Para obter os últimos lançamentos do Magisk",
        "usage": "{tr}magisk",
    },
)
async def kakashi(event):
    "Obtenha os últimos lançamentos da Magisk"
    magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk-files/"
    magisk_dict = {
        "⦁ **Stable**": magisk_repo + "master/stable.json",
        "⦁ **Beta**": magisk_repo + "master/beta.json",
        "⦁ **Canary**": magisk_repo + "master/canary.json",
    }
    releases = "`Últimas versões do magisk:`\n\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [APK v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[Changelog]({data["magisk"]["note"]})\n'
        )
    await edit_or_reply(event, releases)


@catub.cat_cmd(
    pattern="device(?: |$)(\S*)",
    command=("device", plugin_category),
    info={
        "header": "Para obter o nome/modelo do dispositivo Android a partir de seu codinome",
        "usage": "{tr}device <codename>",
        "examples": "{tr}device rav",
    },
)
async def device_info(event):
    "obter o nome do dispositivo Android a partir de seu codinome"
    textx = await event.get_reply_message()
    codename = event.pattern_match.group(1)
    if not codename:
        if textx:
            codename = textx.text
        else:
            return await edit_delete(event, "`Uso: .device <codinome> / <modelo>`")
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Resultados da busca por {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Marca**: {item['brand']}\n"
                f"**Nome**: {item['name']}\n"
                f"**Modelo**: {item['model']}\n\n"
            )
    else:
        reply = f"`Não foi possível encontrar informações sobre {codename}!`\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="codename(?: |)([\S]*)(?: |)([\s\S]*)",
    command=("codename", plugin_category),
    info={
        "header": "Para pesquisar o codinome do dispositivo Android",
        "usage": "{tr}codename <marca> <celular>",
        "examples": "{tr}codename Motorola Moto G8",
    },
)
async def codename_info(event):
    textx = await event.get_reply_message()
    brand = event.pattern_match.group(1).lower()
    device = event.pattern_match.group(2).lower()

    if brand and device:
        pass
    elif textx:
        brand = textx.text.split(" ")[0]
        device = " ".join(textx.text.split(" ")[1:])
    else:
        return await edit_delete(event, "`Uso: .codename <marca> <celular>`")

    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_brand.json"
        ).text
    )
    devices_lower = {k.lower(): v for k, v in data.items()}
    devices = devices_lower.get(brand)
    if not devices:
        return await edit_or_reply(event, f"__Não consegui encontrar {brand}.__")
    results = [
        i
        for i in devices
        if i["name"].lower() == device.lower() or i["model"].lower() == device.lower()
    ]
    if results:
        reply = f"**Resultados da busca por {marca} {celular}**:\n\n"
        if len(results) > 8:
            results = results[:8]
        for item in results:
            reply += (
                f"**Celular**: {item['device']}\n"
                f"**Nome**: {item['name']}\n"
                f"**Modelo**: {item['model']}\n\n"
            )
    else:
        reply = f"`Não consegui encontrar {device} codinome!`\n"
    await edit_or_reply(event, reply)


@catub.cat_cmd(
    pattern="twrp(?: |$)(\S*)",
    command=("twrp", plugin_category),
    info={
        "header": "Para obter os links de download mais recentes do twrp para o dispositivo Android.",
        "usage": "{tr}twrp <codename>",
        "examples": "{tr}twrp vayu",
    },
)
async def twrp(event):
    "obter dispositivo android twrp"
    textx = await event.get_reply_message()
    device = event.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        return await edit_delete(event, "`Uso: .twrp <codinome>`")
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Não foi possível encontrar downloads de twrp para {device}!`\n"
        return await edit_delete(event, reply)
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Última versão do TWRP para {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Atualização:** __{date}__\n"
    )
    await edit_or_reply(event, reply)
