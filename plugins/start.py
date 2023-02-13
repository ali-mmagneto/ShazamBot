from pyrogram import Client, filters

@Client.on_message(filters.command('start'))
async def start_mesaj(bot, message):
    await bot.send_photo(
        chat_id = message.chat.id,
        photo = "https://telegra.ph/file/d24d04e8e605d3eb81b35.jpg",
        caption = "Bu bot sayesinde Telegramdaki her hangi bir video veya ses dosyasını Shazam'da taratarak hangi şarkı olduğunu bulabilirsin :)\n\nhadi durma bir videoyu veya ses dosyasını /shazam komutu ile yanıtla") 
