# Coded by :d (t.me/mmagneto)
from pyrogram import Client, filters
from shazamio import Shazam
import json
import telegraph
from telegraph import Telegraph
import requests

telegraph = Telegraph()
telegraph.create_account(short_name='deprembot')

@Client.on_message(filters.command('shazam'))
async def shazamtara(bot, message):
    try:
        if not message.reply_to_message:
            await message.reply_text("`Bir ses veya videoyu yanıtla...`")
        elif message.reply_to_message.audio or message.reply_to_message.video:
            mes = await message.reply_text("`Shazamda Arıyorum...`")
            ses = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"{message.chat.id}.mp3")
            splitpath = ses.split("/downloads/")
            sestemp = splitpath[1]
            aranacak = f"downloads/{sestemp}"
            shazam = Shazam()
            out = await shazam.recognize_song(aranacak)
            await mes.edit("`Buldum Bilgileri Getiriyorum..`") 
            bilgi = json.dumps(out)
            bilgiler = json.loads(bilgi)
            print(bilgiler)
            i = bilgiler["track"]
            photo = f"{i['images']['coverart']}"
            lyrics = f"{i['sections'][1]['text']}"
            print(lyrics)
            satir = "\n"
            sarki = f"{i['title']}" 
            link = telegraph.create_page(
                    f"{sarki} Sözleri :d",
                    html_content=lyrics)
            text = f"**Şarkı**: [{i['title']}]({i['share']['href']})\n**Sanatçı**: {i['subtitle']}\n**Shazam İd**: {i['key']}\n**Lyrics**: {link['url']}"
            await bot.send_photo(
                chat_id = message.chat.id, 
                photo = photo, 
                caption = text)
            await mes.delete()
        elif message.reply_to_message.text:
            linkim = message.reply_to_message.text
            print(linkim)
            url = "https://tiktok-download-video-no-watermark.p.rapidapi.com/tiktok/info"
            querystring = {"url": f"{linkim}"}

            headers = {
                    'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
                    'x-rapidapi-key': "f9d65af755msh3c8cac23b52a5eep108a33jsnbf7de971bb72"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
        else:
            await message.reply_text("`Bir ses veya videoyu yanıtla...`")
    except Exception as e:
        await message.reply_text(f"`{e}`")
