import asyncio

from userbot import catub

from ..core.managers import edit_or_reply

plugin_category = "fun"


@catub.cat_cmd(
    pattern="^\:/$",
    command=("\:", plugin_category),
    info={
        "header": "Animation command",
        "usage": "\:",
    },
)
async def kek(keks):
    "Animation command"
    keks = await edit_or_reply(keks, ":\\")
    uio = ["/", "\\"]
    for i in range(15):
        await asyncio.sleep(0.5)
        txt = ":" + uio[i % 2]
        await keks.edit(txt)


@catub.cat_cmd(
    pattern="^\-_-$",
    command=("-_-", plugin_category),
    info={
        "header": "Animation command",
        "usage": "-_-",
    },
)
async def lol(lel):
    "Animation command"
    lel = await edit_or_reply(lel, "-__-")
    okay = "-__-"
    for _ in range(15):
        await asyncio.sleep(0.5)
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@catub.cat_cmd(
    pattern="^\;_;$",
    command=(";_;", plugin_category),
    info={
        "header": "Animation command",
        "usage": ";_;",
    },
)
async def fun(e):
    "Animation command"
    e = await edit_or_reply(e, ";__;")
    t = ";__;"
    for _ in range(15):
        await asyncio.sleep(0.5)
        t = t[:-1] + "_;"
        await e.edit(t)


@catub.cat_cmd(
    pattern="oof$",
    command=("oof", plugin_category),
    info={
        "header": "Animation command",
        "usage": "{tr}oof",
    },
)
async def Oof(e):
    "Animation command."
    t = "Oof"
    catevent = await edit_or_reply(e, t)
    for _ in range(20):
        await asyncio.sleep(0.1)
        t = t[:-1] + "of"
        await catevent.edit(t)


@catub.cat_cmd(
    pattern="k$",
    command=("k", plugin_category),
    info={
        "header": "Animation command",
        "usage": "{tr}k",
    },
)
async def K(e):
    "Animation command."
    t = "K"
    catevent = await edit_or_reply(e, t)
    for _ in range(20):
        await asyncio.sleep(0.1)
        t = t[:-1] + "KKK"
        await catevent.edit(t)


@catub.cat_cmd(
    pattern="type ([\s\S]*)",
    command=("type", plugin_category),
    info={
        "header": "Type writter animation.",
        "usage": "{tr}type text",
    },
)
async def typewriter(typew):
    "Type writter animation."
    message = typew.pattern_match.group(1)
    sleep_time = 0.2
    typing_symbol = "|"
    old_text = ""
    typew = await edit_or_reply(typew, typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)


@catub.cat_cmd(
    pattern="repeat (\d*) ([\s\S]*)",
    command=("repeat", plugin_category),
    info={
        "header": "repeats the given text with given no of times.",
        "usage": "{tr}repeat <count> <text>",
        "examples": "{tr}repeat 10 catuserbot",
    },
)
async def _(event):
    "To repeat the given text."
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    count = int(cat[0])
    repsmessage = (f"{message} ") * count
    await edit_or_reply(event, repsmessage)


@catub.cat_cmd(
    pattern="meme",
    command=("meme", plugin_category),
    info={
        "header": "Animation command",
        "usage": [
            "{tr}meme <emoji/text>",
            "{tr}meme",
        ],
    },
)
async def meme(event):
    "Animation command."
    memeVar = event.text
    sleepValue = 0.5
    memeVar = memeVar[6:]
    if not memeVar:
        memeVar = "✈️"
    event = await edit_or_reply(event, "-------------" + memeVar)
    await asyncio.sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await asyncio.sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await asyncio.sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await asyncio.sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await asyncio.sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await asyncio.sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await asyncio.sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await asyncio.sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await asyncio.sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await asyncio.sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await asyncio.sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await asyncio.sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await asyncio.sleep(sleepValue)
    await event.edit("-------------" + memeVar)
    await asyncio.sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await asyncio.sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await asyncio.sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await asyncio.sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await asyncio.sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await asyncio.sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await asyncio.sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await asyncio.sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await asyncio.sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await asyncio.sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await asyncio.sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await asyncio.sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar)


@catub.cat_cmd(
    pattern="give",
    command=("give", plugin_category),
    info={
        "header": "Animation command",
        "usage": [
            "{tr}give <emoji/text>",
            "{tr}give",
        ],
    },
)
async def give(event):
    "Animation command."
    giveVar = event.text
    sleepValue = 0.5
    lp = giveVar[6:]
    if not lp:
        lp = " 🍭"
    event = await edit_or_reply(event, lp + "        ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)
    await asyncio.sleep(sleepValue)
    await event.edit(lp + "        ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)


@catub.cat_cmd(
    pattern="sadmin$",
    command=("sadmin", plugin_category),
    info={
        "header": "Shouts Admin Animation command",
        "usage": "{tr}sadmin",
    },
)
async def _(event):
    "Shouts Admin Animation command."
    animation_ttl = range(13)
    event = await edit_or_reply(event, "sadmin")
    animation_chars = [
        "@aaaaaaaaaaaaadddddddddddddmmmmmmmmmmmmmiiiiiiiiiiiiinnnnnnnnnnnnn",
        "@aaaaaaaaaaaaddddddddddddmmmmmmmmmmmmiiiiiiiiiiiinnnnnnnnnnnn",
        "@aaaaaaaaaaadddddddddddmmmmmmmmmmmiiiiiiiiiiinnnnnnnnnnn",
        "@aaaaaaaaaaddddddddddmmmmmmmmmmiiiiiiiiiinnnnnnnnnn",
        "@aaaaaaaaadddddddddmmmmmmmmmiiiiiiiiinnnnnnnnn",
        "@aaaaaaaaddddddddmmmmmmmmiiiiiiiinnnnnnnn",
        "@aaaaaaadddddddmmmmmmmiiiiiiinnnnnnn",
        "@aaaaaaddddddmmmmmmiiiiiinnnnnn",
        "@aaaaadddddmmmmmiiiiinnnnn",
        "@aaaaddddmmmmiiiinnnn",
        "@aaadddmmmiiinnn",
        "@aaddmmiinn",
        "@admin",
    ]
    for i in animation_ttl:
        await asyncio.sleep(1)
        await event.edit(animation_chars[i % 13])


@catub.cat_cmd(
    pattern="fds$",
    command=("fds", plugin_category),
    info={
        "header": "Foda-se?",
        "usage": "{tr}fds",
    },
)
async def iqless(e):
    "Foda-se?"
    await edit_or_reply(e, "F\n"
"     O\n"
"　　 O\n"
"　　　O\n"
"　　　 o\n"
"ₒ ᵒ 。   o\n"
"ᵒ ₒ °ₒ  ᵒ\n"
"　 ˚\n"
"　°\n"
"　•\n"
"　 .\n"
"　　.   \n"
"           da-se?")


@catub.cat_cmd(
    pattern="sexo$",
    command=("sexo", plugin_category),
    info={
        "header": "kkkkkkkhkkkkk sexo bixo",
        "usage": "{tr}sexo",
    },
)
async def _(event):
    "Mostra um meme sexokkkkkkkk."
    animation_ttl = range(4)
    event = await edit_or_reply(event, "sexo?")
    animation_chars = [
        "HOLY SHIT!!",
        "IS THAT A\n"
"MOTHERFUCKING\n"
"█▀▀ █▀▀ █─█ █▀▀█ \n"
"▀▀█ █▀▀ ▄▀▄ █──█ \n"
"▀▀▀ ▀▀▀ ▀─▀ ▀▀▀▀\n"
"           REFERENCE???",
        "Perai...é aqui que estão falando de...",
        "KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"KKKK\n"
"KKKK\n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"               KKKK\n"
"               KKKK\n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"  \n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"KKKK\n"
"KKKK\n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"KKKK\n"
"KKKK\n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"  \n"
"KKKK       KKKK\n"
" KKKK    KKKK\n"
"   KKKK KKKK\n"
"      KKKKKK\n"
"      KKKKKK\n"
"      KKKKKK\n"
"  KKKK     KKKK\n"
"KKKK        KKKK\n"
"  \n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"KKKK     KKKK\n"
"KKKK     KKKK\n"
"KKKK     KKKK\n"
"KKKK     KKKK\n"
"KKKKKKKKKK\n"
"KKKKKKKKKK\n"
"  \n"
"  KKKKKKKK\n"
"KKKKKKKKKK\n"
"KKK        KKK\n"
"              KKK\n"
"            KKK\n"
"          KKK\n"
"        KKK\n"
"      KKK\n"  
"      KKK\n"   
"    \n"
"      KKK\n"
"      KKK",
    ]
    for i in animation_ttl:
        await asyncio.sleep(2)
        await event.edit(animation_chars[i % 4])


@catub.cat_cmd(
    pattern="pqp$",
    command=("pqp", plugin_category),
    info={
        "header": "Puta que pariu",
        "usage": "{tr}pqp",
    },
)
async def iqless(e):
    "Puta que pariu"
    await edit_or_reply(e, "**PUTA QUE PARIU, HEIN**")


@catub.cat_cmd(
    pattern="milior$",
    command=("milior", plugin_category),
    info={
        "header": "CR7 PIKA",
        "usage": "{tr}milior",
    },
)
async def iqless(e):
    "Milior"
    await edit_or_reply(e, "`Eu sou o milior posso num ser mas, em minha cabeça eu sou o milior`\n"
"⠀⠀⠀⠀⢀⣠⠤⡶⣲⢺⣴⣶⢭⣉⢲⣀⠀⠀⠀⠀⠀⠀⠀⠀\n"
"⠀⠀⢀⡾⢵⣶⣿⣿⣿⣾⣷⣳⣿⣷⣵⣈⠷⢤⡀⠀⠀⠀⠀⠀\n"
"⠀⠀⠘⢾⣿⡿⠿⠿⠿⠿⠿⠿⢿⡿⣿⣿⣿⣾⣾⣦⠀⠀⠀⠀\n"
"⠀⠀⣠⡋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⢿⣧⠀⠀⠀\n"
"⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣳⢮⣧⠀⠀\n"
"⢠⣧⠇⡠⠄⣤⣤⣄⡀⠀⠀⣀⣤⣄⣤⣀⠀⠀⣿⣿⣿⣯⣇⠀\n"
"⠈⣿⠀⢀⣶⣾⣿⣿⠁⠀⢸⣿⣿⣿⣧⣌⣥⠀⠘⣿⣿⣿⣿⠀\n"
"⢀⣿⠀⠈⠁⠀⠀⠁⠀⠀⠀⠉⠉⠭⠽⠿⠻⠁⠀⣿⣿⣿⡏⠀\n"
"⡏⠆⠀⠀⠀⠀⠀⠀⡀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⢋⣿⣆\n"
"⡎⠀⠀⢀⡴⠂⠈⠉⠻⠿⠿⠛⣀⢲⣤⣄⣀⠀⠀⠈⠘⣏⢹⡿\n"
"⠱⡄⠘⢻⣳⣤⡶⠖⠒⠶⠶⢶⣿⣷⣿⣿⣿⣟⠀⠀⠄⠠⣰⠃\n"
"⠀⢹⠀⠀⠀⠈⠓⠒⠒⠒⠒⠒⠛⠁⢨⣼⣿⣿⡀⣼⠖⠛⠁⠀\n"
"⠀⠘⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⢁⠀⠀⠀⠀⠀\n"
"⠀⠀⢸⠀⠀⠀⢀⣀⣀⣀⣠⣤⣶⣿⣿⣿⡿⣁⡎⢸⠀⠀⠀⠀\n"
"⠀⠀⢸⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠸⠀⠀⠀⠀\n"
"⠀⠀⢸⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⡄⠀⡇⠀⠀⠀\n"
"⠀⢀⣼⠀⠀⠀⠀⠀⠈⢹⣿⣿⣿⡟⣿⣿⣿⣟⡁⠀⢿⣷⡄⠀\n"
"⠀⣸⣿⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣝⣿⣿⡍⠁⠀⢸⣿⣷⠀\n"
"⠀⣿⣿⡀⠀⠀⠀⠀⠀⢐⣿⣿⣿⣿⣿⣿⣯⠁⠀⠀⢸⣿⣿⠀\n"
"⠀⢿⢿⣿⣄⠀⠀⠀⠀⢼⣿⣿⣿⣿⣿⣿⡯⠀⢠⢒⣿⣿⡏⠀\n"
"⠀⠈⢮⡻⣿⣷⣀⠀⢀⢸⣿⣿⣟⣿⣿⠿⠒⣀⣤⣿⣿⠏⠀⠀\n"
"⠀⠀⠀⠙⠺⣿⣿⣿⣾⣾⣿⣭⣭⣭⣷⣾⣿⣿⣿⠟⠁⠀⠀⠀\n"
"⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠿⠿⠟⠛⠉⠁⠀⠀⠀⠀⠀")


@catub.cat_cmd(
    pattern="kk$",
    command=("kk", plugin_category),
    info={
        "header": "Animation command",
        "usage": "{tr}kk",
    },
)
async def K(e):
    "Animation command."
    t = "K"
    catevent = await edit_or_reply(e, t)
    for _ in range(30):
        await asyncio.sleep(0.1)
        t = t[:-1] + "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK"
        await catevent.edit(t)
