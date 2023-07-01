import asyncio
import datetime
import json
from aiogram import Dispatcher, Router, types, Bot
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from app.apps.core.bot.parsing.main import check_news_update

from app.apps.core.use_case import CORE_USE_CASE
from app.config.application import INSTALLED_APPS
from app.apps.core.bot.data.config import ADMINS
from app.config.bot import TG_TOKEN

router = Router()
bot = Bot(TG_TOKEN, parse_mode="HTML")

async def is_admin(user_id: int):

    return user_id in ADMINS

@router.message(Command(commands=["start"]))
async def handle_start_command(message: Message) -> None:

    

    if message.from_user is None:
        return

    _, is_new = await CORE_USE_CASE.register_bot_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
    )

    if is_new:
        await message.answer(f"Welcome Dalboyob!\n\n{message.from_user.username}")
    else:
        await message.answer(f"Poshol Naxuy!!!\n\n {message.from_user.username}")

    kb = [
        [
            types.KeyboardButton(text="Все новости"),
            types.KeyboardButton(text="Последние 5 новостей"),
        ],
        [types.KeyboardButton(text="Свежие новости")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(text="Лента новостей", reply_markup=keyboard)

@router.message(Text(text="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        # news = f"<b>{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}</b>\n" \
        #        f"<u>{v['article_title']}</u>\n" \
        #        f"<code>{v['article_desc']}</code>\n" \
        #        f"{v['article_url']}"
        # news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
        #        f"{hunderline(v['article_title'])}\n" \
        #        f"{hcode(v['article_desc'])}\n" \
        #        f"{hlink(v['article_title'], v['article_url'])}"
        news = f"{hbold(v['article_date_timestamp'])}\n" \
               f"{hlink(v['article_title'], v['article_url'])}"

        await message.answer(news)


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(v['article_date_timestamp'])}\n" \
                    f"{hlink(v['article_title'], v['article_url'])}"

                # get your id @userinfobot
                user_id = 984573662
                await bot.send_message(user_id=user_id, text=news)

        else:
            await bot.send_message(ADMINS, "Пока нет свежих новостей...")

        await asyncio.sleep(4)

@router.message(Command(commands=["apps"]))
async def handle_apps_command(message: Message) -> None:

    if await is_admin(message.from_user.id):

        await message.answer("Welcome, admin!")
        apps_names = [app_name for app_name in INSTALLED_APPS if app_name.startswith("app.")]
        await message.answer("Installed apps:\n" f"{apps_names}")
    else:
        await message.answer("chmo sen admin emassan!!!.")




@router.message(Command(commands=["id"]))
async def handle_id_command(message: Message) -> None:
    if message.from_user is None:
        return

    await message.answer(
        f"User Id: <b>{message.from_user.id}</b>\n" f"Chat Id: <b>{message.chat.id}</b>"
    )
