#By @feelded
import requests
from userbot import catub
from ..core.managers import edit_or_reply, edit_delete

plugin_category = "useless"

@catub.cat_cmd(
    pattern="letra ?(.*)",
    command=("letra", plugin_category),
    info={
        "header": "Pesquisa de letras de músicas",
        "description": "se você quiser fornecer o nome do artista com o nome da música, será melhor",
        "usage": [
            "{tr}letra <nome da música>",
        ],
        "examples": [
            "{tr}letra death bed",
        ],
    },
)
async def lyrics(odi):
    "To get song lyrics"
    songname = odi.pattern_match.group(1)
    if not songname:
    	await edit_delete(odi, "`Coloque o nome de uma música`", 6)
    else:
    	await edit_or_reply(odi, f"`Procurando letras por {songname} ...`")
    	x = requests.get(f'https://botzhub.herokuapp.com/lyrics?song={songname}').json()
    	artist = lyrics = ""
    	try:
    		artist = x['artist']
    		lyrics = x['lyrics']
    	except:
    		lyrics = x['lyrics']
    	
    		if artist == "":
    			await edit_or_reply(odi, f"**Música:** `{songname}`\n\n`{lyrics}`")
    		else:
    			await edit_or_reply(odi, f"**Música:** `{songname}`\n**Artista:** {artist}\n\n`{lyrics}`")
