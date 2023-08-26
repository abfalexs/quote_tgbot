import dns.resolver
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

client = MongoClient(os.getenv('MONGODB_TOKEN'))
db = client["tgbot"]
collection = db["collection_quotes"]

bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button = [[types.KeyboardButton(text='/quote')]]
    menu = types.ReplyKeyboardMarkup(keyboard=button,
                                     input_field_placeholder='Отправить цитату по кнопке')

    await message.reply(
        "Привет! Я бот с мотивационными цитатами и цитатами известных личностей. Нажми кнопку /quote чтобы получить цитату.", reply_markup=menu)


@dp.message_handler(commands=['quote'])
async def quote(message: types.Message):
    quote_doc = collection.aggregate([{"$sample": {"size": 1}}])
    result = list(quote_doc)
    if result:
        quote_text = result[0]["quote"]
        await message.reply(quote_text)
    else:
        await message.reply("К сожалению, нет доступных цитат.")


async def main():
    await dp.start_polling()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
