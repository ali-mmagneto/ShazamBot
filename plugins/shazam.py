# Coded by :d (t.me/mmagneto)
from pyrogram import Client, filters
from shazamio import Shazam
import json
from youtube_search import YoutubeSearch
import telegraph
from telegraph import Telegraph
import requests
import os, youtube_dl, requests, time


telegraph = Telegraph()
telegraph.create_account(short_name='ShazamBot')

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
            unlu = f"{i['subtitle']}" 
            link = telegraph.create_page(
                    f"{sarki} Sözleri :d",
                    html_content=lyrics)
            text = f"**Şarkı**: [{i['title']}]({i['share']['href']})\n**Sanatçı**: {i['subtitle']}\n**Shazam İd**: {i['key']}\n**Lyrics**: {link['url']}"
            await bot.send_photo(
                chat_id = message.chat.id, 
                photo = photo, 
                caption = text)
            await mes.delete()
            ydl_opts = {"format": "bestaudio[ext=mp3]"}
            try:
                query = f"{unlu} {sarki}"
                results = []
                count = 0
                while len(results) == 0 and count < 6:
                    if count>0:
                        time.sleep(1)
                    results = YoutubeSearch(query, max_results=1).to_dict()
                    count += 1
                try:
                    link = f"https://youtube.com{results[0]['url_suffix']}"
                    title = results[0]["title"]
                    thumbnail = results[0]["thumbnails"][0]
                    duration = results[0]["duration"]
                    views = results[0]["views"]
                    thumb_name = f'thumb{message.message_id}.jpg'
                    thumb = requests.get(thumbnail, allow_redirects=True)
                    open(thumb_name, 'wb').write(thumb.content)
                except Exception as e:
                    print(e)
                    return
            except Exception as e:
                print(str(e))
                return
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                    audio_file = ydl.prepare_filename(info_dict)
                    ydl.process_info(info_dict)
                rep = "ShazamBot"
                secmul, dur, dur_arr = 1, 0, duration.split(':')
                for i in range(len(dur_arr)-1, -1, -1):
                    dur += (int(dur_arr[i]) * secmul)
                    secmul *= 60
                message.reply_audio(audio_file, caption=rep, quote=False, title=title, duration=dur, thumb=thumb_name, performer="ShazamBot")
            except Exception as e:
                print(e)
        else:
            await message.reply_text("`Bir ses veya videoyu yanıtla...`")
    except Exception as e:
        await message.reply_text(f"`{e}`")
