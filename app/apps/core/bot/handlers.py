from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.apps.core.use_case import CORE_USE_CASE
from app.config.application import INSTALLED_APPS
from app.apps.core.bot.data.config import ADMINS


router = Router()

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
