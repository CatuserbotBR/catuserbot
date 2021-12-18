# Credits of Plugin @ViperAdnan and @mrconfused(revert)[will add sql soon]
import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

from ..Config import Config
from . import (
    ALIVE_NAME,
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    catub,
    edit_delete,
    get_user_from_event,
)

plugin_category = "utils"
DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = (
    str(DEFAULT_BIO)
    if DEFAULT_BIO
    else ""
)


@catub.cat_cmd(
    pattern="clone(?:\s|$)([\s\S]*)",
    command=("clone", plugin_category),
    info={
        "header": "Para clonar a conta do usuário mencionado ou do usuário respondido",
        "usage": "{tr}clone <nome/id/resposta>",
    },
)
async def _(event):
    "Para clonar a conta do usuário mencionado ou do usuário respondido"
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌"
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    try:
        pfile = await event.client.upload_file(profile_pic)
    except Exception as e:
        return await edit_delete(event, f"** Falha ao clonar devido a erro:**\n__{e}__")
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await edit_delete(event, "**Eu sou você e você é eu, somos um só.**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#CLONED\nclonado com sucesso [{first_name}](tg://user?id={user_id })",
        )


@catub.cat_cmd(
    pattern="revert$",
    command=("revert", plugin_category),
    info={
        "header": "Para voltar ao seu nome original, biografia e foto do perfil",
        "note": "Para o funcionamento adequado deste comando, você precisa definir AUTONAME e DEFAULT_BIO com seu nome de perfil e bio, respectivamente.",
        "usage": "{tr}revert",
    },
)
async def _(event):
    "Para redefinir seus detalhes originais"
    name = f"{DEFAULTUSER}"
    blank = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=blank))
    await edit_delete(event, "**Revertido com sucesso para sua conta original.**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#REVERT\nrevertido com sucesso para o seu perfil original",
        )
