from telethon import TelegramClient, events
from dotenv import dotenv_values
from src.utils.main_logger import log_data, log_error
from src.process import train_model, predict_sentiment

from pprint import pprint 

env = dotenv_values(".env")

bot = TelegramClient(
    "testingbot",
    env["API_ID"],
    env["API_HASH"],
).start(
    bot_token=env["BOT_TOKEN"]
)

@bot.on(events.NewMessage(pattern='/start'))
async def start_func(event):
    """send message when new message is received"""
    await event.reply("Hello, selamat datang di bot saya")

@bot.on(events.NewMessage(pattern='/testing'))
async def testing_func(event):
    """send message when new message is received"""

    pprint(event.message.to_dict())

    await event.respond("Hello, selamat datang di bot saya")

@bot.on(events.NewMessage(pattern='/hitung'))
async def hitung_func(event):
    """send message when new message is received"""

    list_num = event.text.split()[1]
    log_data(f"data input dari hitung: {list_num}")
    result = eval(list_num)
    result = sum(result)

    await event.reply(f"Hasil penjumlahan dari {list_num} adalah {result}")

@bot.on(events.NewMessage(pattern='#latih_model'))
async def model_training_func(event):
    '''melakukan training model dari analisis sentiment'''

    result = train_model()

    await event.respond(f"{result}")

@bot.on(events.NewMessage(pattern='#prediksi_sentiment'))
async def predict_sentiment_func(event):
    '''melakukan training model dari analisis sentiment'''
    
    data = " ".join(event.text.split()[1:])
    log_data(f"[PREDIKSI] data input: {data}")

    result = predict_sentiment(data)
    log_data(f"[PREDIKSI] hasil prediksi: {result}")

    await event.respond(f"hasil dari analisis sentiment untuk kalimat tersebut adalah :{result}")

def run():
    """start a bot"""
    print("aplikasi telah berjalan")
    bot.run_until_disconnected()