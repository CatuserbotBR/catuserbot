from asyncio import sleep

from googletrans import LANGUAGES, Translator

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, deEmojify

plugin_category = "utils"

# https://github.com/ssut/py-googletrans/issues/234#issuecomment-722379788
async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


@catub.cat_cmd(
    pattern="tl ([\s\S]*)",
    command=("tl", plugin_category),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl te ; Catuserbot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "pt"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "`.tl LanguageCode` as reply to a message", time=5
        )
    text = deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"**Traduzido de {LANGUAGES[translated.src].title()} para {LANGUAGES[lan].title()}**\
                \n`{after_tr_text}`"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**Error:**\n`{exc}`", time=5)


@catub.cat_cmd(
    pattern="tr(?: |$)([\s\S]*)",
    command=("tr", plugin_category),
    info={
        "header": "To translate the text to required language.",
        "note": "for this set command set lanuage by `{tr}lang tr` command.",
        "usage": [
            "{tr}tr",
            "{tr}tr <text>",
        ],
    },
)
async def translateme(trans):
    "To translate the text to required language."
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        return await edit_or_reply(
            trans, "`Give a text or reply to a message to translate!`"
        )
    TR_LANG = gvarstatus("TR_LANG") or "pt"
    try:
        reply_text = await getTranslate(deEmojify(message), dest=TR_LANG)
    except ValueError:
        return await edit_delete(trans, "`Invalid destination language.`", time=5)
    source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
    transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
    reply_text = f"**De {source_lan.title()}({reply_text.src.lower()}) para {transl_lan.title()}({reply_text.dest.lower()}) :**\n`{reply_text.text}`"

    await edit_or_reply(trans, reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"`Traduzido algumas coisas de {source_lan.title()} para {transl_lan.title()} agora mesmo.`",
        )


@catub.cat_cmd(
    pattern="lang (ai|tr|tocr) ([\s\S]*)",
    command=("lang", plugin_category),
    info={
        "header": "To set language for tr/ai command.",
        "description": "Check here [Language codes](https://bit.ly/2SRQ6WU)",
        "options": {
            "tr": "default language for tr command",
            "ai": "default language for chatbot(ai)",
            "tocr": "default language for tocr command",
        },
        "usage": "{tr}lang option <language codes>",
        "examples": [
            "{tr}lang tr te",
            "{tr}lang ai hi",
            "{tr}lang tocr en",
        ],
    },
)
async def lang(value):
    "To set language for tr comamnd."
    arg = value.pattern_match.group(2).lower()
    input_str = value.pattern_match.group(1)
    if arg not in LANGUAGES:
        return await edit_or_reply(
            value,
            f"`Invalid Language code !!`\n`Available language codes for TR`:\n\n`{LANGUAGES}`",
        )
    LANG = LANGUAGES[arg]
    if input_str == "tr":
        addgvar("TR_LANG", arg)
        await edit_or_reply(
            value, f"`Language for Translator changed to {LANG.title()}.`"
        )
    elif input_str == "tocr":
        addgvar("TOCR_LANG", arg)
        await edit_or_reply(
            value, f"`Language for Translated Ocr changed to {LANG.title()}.`"
        )
    else:
        addgvar("AI_LANG", arg)
        await edit_or_reply(
            value, f"`Language for chatbot is changed to {LANG.title()}.`"
        )
    LANG = LANGUAGES[arg]

    if BOTLOG and input_str == "tr":
        await value.client.send_message(
            BOTLOG_CHATID, f"`Language for Translator changed to {LANG.title()}.`"
        )
    if BOTLOG:
        if input_str == "tocr":
            await value.client.send_message(
                BOTLOG_CHATID,
                f"`Language for Translated Ocr changed to {LANG.title()}.`",
            )
        if input_str == "ai":
            await value.client.send_message(
                BOTLOG_CHATID, f"`Language for chatbot is changed to {LANG.title()}.`"
            )
