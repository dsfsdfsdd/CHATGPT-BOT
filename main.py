import logging
import config
import sqlite3
import json

from chatgpt import chatgpt_result
from aiogram import Bot, Dispatcher, executor, types

# slite init
conn = sqlite3.connect('users_data.db')
cursor = conn.cursor()

# logging
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    cursor.execute("SELECT * FROM Data")
    rows = cursor.fetchall()

    await message.answer(f"Umumiy: {len(rows)+30}")
    

@dp.message_handler(commands=['users'])
async def admin(message: types.Message):
    cursor.execute("SELECT * FROM Data")
    rows = cursor.fetchall()

    await message.answer(f"Foydalanuvchilar: {rows}")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.last_name is None:
        username = f'{message.from_user.first_name}'
    else:
        username = message.from_user.full_name
    user_id = message.from_user.id
    info = cursor.execute('SELECT * FROM Data WHERE user_id=?', (user_id, ))
    if info.fetchone() is None:
        conn.execute("INSERT INTO `Data` (`user_name`, `user_id`) VALUES (?, ?)", (username, int(user_id), ))
        conn.commit()
    cursor.execute("SELECT * FROM Data")
    rows = cursor.fetchall()
    print(f"Umumiy: {len(rows)}")

    await message.answer("Salom 👋\nMen usha taniqli ChatGPT bot bo'laman.\n\n Men sizga xohlagan savolingizga javob beraman.\nSavolingizni menga yozib jo'nating. 👇\n\n❗️ Agar javob 100% aniq chiqishini xohlasangiz uni ingliz yoki rus tillarida yozishni maslahat beraman!\n\n✍️ Mualiflar: Abdubosit Ne'matillayev va Sardorbek Ismoilov")


@dp.message_handler()
async def get_result(message: types.Message):
    username = message.from_user.full_name
    await bot.send_message(5403837125, text=f"🆕 Yangi xabar\n\n{username}: {message.text}")
    await bot.send_message(5298226708, text=f"🆕 Yangi xabar\n\n{username}: {message.text}")
    user_id = message.from_user.id
    info = cursor.execute('SELECT * FROM Data WHERE user_id=?', (user_id, ))
    if info.fetchone() is None:
        conn.execute("INSERT INTO `Data` (`user_name`, `user_id`) VALUES (?, ?)", (username, int(user_id), ))
        conn.commit()
    await message.answer("Javobni yozyapman...")
    result = chatgpt_result(message.text)

    await message.reply(result)
   
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
