from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from dotenv import dotenv_values

from datetime import datetime
from pprint import pprint

env = dotenv_values(".env")
bot_token = env['BOT_TOKEN']

async def start_func(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f"Terdapat pesan yang masuk ke handler start.\nIsinya adalah :\n{update.message.text}")
    print("_"*40)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello, salam perkenalan"
    )

async def hitung_func(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f"Terdapat pesan yang masuk ke handler hitung.\nIsinya adalah :\n{update.message.text}")
    print("_"*40)

    list_num = update.message.text.split()[1]
    result = eval(list_num)
    result = sum(result)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hasil Penjumlahan dari {list_num} adalah {result}"
    )

async def testing_func(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f"Terdapat pesan yang masuk ke handler testing.\nIsinya adalah :\n{update.message.text}")
    print("_"*40)

    pprint(update.to_dict())

    # date = datetime.fromtimestamp(int(update.message.date))
    print(f"Tanggal terkirim: {update.message.date}")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"testing"
    )


if __name__ == '__main__':
    #membuat objek aplikasi
    app = Application.builder().token(bot_token).build()

    #membuat objek handler
    start_handler = CommandHandler('start', start_func)
    app.add_handler(start_handler)

    hitung_handler = CommandHandler('hitung', hitung_func)
    app.add_handler(hitung_handler)

    testing_handler = CommandHandler('testing', testing_func)
    app.add_handler(testing_handler)

    print("aplikasi berjalan")
    #menjalankan aplikasinya
    app.run_polling()