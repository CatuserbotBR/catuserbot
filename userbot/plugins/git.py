import os
from datetime import datetime

import aiohttp
import requests
from github import Github
from pySmartDL import SmartDL

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import reply_id

LOGS = logging.getLogger(os.path.basename(__name__))
ppath = os.path.join(os.getcwd(), "temp", "githubuser.jpg")
plugin_category = "misc"

GIT_TEMP_DIR = "./temp/"


@catub.cat_cmd(
    pattern="repo$",
    command=("repo", plugin_category),
    info={
        "header": "Link do código fonte do userbot",
        "usage": [
            "{tr}repo",
        ],
    },
)
async def source(e):
    "Link do código fonte do userbot"
    await edit_or_reply(
        e,
        "[👾\u2063](https://telegra.ph/file/ae86a6ddfa277e6e50101.jpg)Clique [aqui](https://github.com/CatuserbotBR/catuserbot) para abrir o repositório do Catuserbot.",
        link_preview=True",
    )


@catub.cat_cmd(
    pattern="github( -l(\d+))? ([\s\S]*)",
    command=("github", plugin_category),
    info={
        "header": "Mostra as informações sobre um usuário no GitHub com o nome de usuário fornecido",
        "flags": {"-l": "limite de repo: padrão para 5"},
        "usage": ".github [flag] [username]",
        "examples": [".github AGMODDER", ".github -l5 AGMODDER"],
    },
)
async def _(event):
    "Obtenha informações sobre um usuário GitHub"
    reply_to = await reply_id(event)
    username = event.pattern_match.group(3)
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edit_delete(event, "`" + username + " não encontrado`")
            catevent = await edit_or_reply(event, "`buscando informações do github...`")
            result = await request.json()
            photo = result["avatar_url"]
            if result["bio"]:
                result["bio"] = result["bio"].strip()
            repos = []
            sec_res = requests.get(result["repos_url"])
            if sec_res.status_code == 200:
                limit = event.pattern_match.group(2)
                limit = 5 if not limit else int(limit)
                for repo in sec_res.json():
                    repos.append(f"[{repo['name']}]({repo['html_url']})")
                    limit -= 1
                    if limit == 0:
                        break
            REPLY = "**Informações GitHub para** `{username}`\
                \n👤 **Nome:** [{name}]({html_url})\
                \n🔧 **Modelo:** `{type}`\
                \n🏢 **Companhia:** `{company}`\
                \n🔭 **Blog** : {blog}\
                \n📍 **Localização** : `{location}`\
                \n📝 **Bio** : __{bio}__\
                \n❤️ **Seguidores(as)** : `{followers}`\
                \n👁 **Segue** : `{following}`\
                \n📊 **Repositórios Públicos** : `{public_repos}`\
                \n📄 **Síntese Pública** : `{public_gists}`\
                \n🔗 **Perfil Criado** : `{created_at}`\
                \n✏️ **Perfil atualizado** : `{updated_at}`".format(
                username=username, **result
            )

            if repos:
                REPLY += "\n🔍 **Alguns Repositórios** : " + " | ".join(repos)
            downloader = SmartDL(photo, ppath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
            await event.client.send_file(
                event.chat_id,
                ppath,
                caption=REPLY,
                reply_to=reply_to,
            )
            os.remove(ppath)
            await catevent.delete()


@catub.cat_cmd(
    pattern="commit$",
    command=("commit", plugin_category),
    info={
        "header": "Para enviar o plugin respondido ao github.",
        "description": "Ele envia o arquivo fornecido para o seu repositório github em **userbot/plugins** folder\
        \nPara trabalhar com o conjunto de plugins de a confirmação com o `GITHUB_ACCESS_TOKEN` e `GIT_REPO_NAME` Variáveis ​​no Heroku vars First",
        "note": "A partir de agora, não é necessário, com certeza vou desenvolvê-lo ",
        "usage": "{tr}commit",
    },
)
async def download(event):
    "Para enviar o plugin respondido ao github."
    if Config.GITHUB_ACCESS_TOKEN is None:
        return await edit_delete(
            event, "`ADICIONE o token de acesso adequado de github.com`", 5
        )
    if Config.GIT_REPO_NAME is None:
        return await edit_delete(
            event, "`ADICIONE o nome adequado do repositório Github do seu userbot`", 5
        )
    mone = await edit_or_reply(event, "`Processando ...`")
    if not os.path.isdir(GIT_TEMP_DIR):
        os.makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    if not reply_message or not reply_message.media:
        return await edit_delete(
            event, "__Responda a um arquivo que você deseja enviar em seu github.__"
        )
    try:
        downloaded_file_name = await event.client.download_media(reply_message.media)
    except Exception as e:
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            "Baixado para `{}` dentro de {} segundos.".format(downloaded_file_name, ms)
        )
        await mone.edit("Fazendo o commit no Github....")
        await git_commit(downloaded_file_name, mone)


async def git_commit(file_name, mone):
    content_list = []
    access_token = Config.GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name, "r", encoding="utf-8")
    commit_data = file.read()
    repo = g.get_repo(Config.GIT_REPO_NAME)
    LOGS.info(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        LOGS.info(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="' + file_name + '")':
            return await mone.edit("`O arquivo já existe`")
    if create_file:
        file_name = "userbot/plugins/" + file_name
        LOGS.info(file_name)
        try:
            repo.create_file(
                file_name, "Enviado Novo Plugin", commit_data, branch="master"
            )
            LOGS.info("Feito o commit do arquivo")
            ccess = Config.GIT_REPO_NAME
            ccess = ccess.strip()
            await mone.edit(
                f"`Commit feito em seu repositório Github`\n\n[Your PLUGINS](https://github.com/{ccess}/tree/master/userbot/plugins/)"
            )
        except BaseException:
            LOGS.info("Não é possível criar o plugin")
            await mone.edit("Não é possível enviar o plugin")
    else:
        return await mone.edit("`Commit suicidado`")
