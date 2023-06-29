from aiogram import types
from aiogram.filters import Filter

from app.apps.core.bot.data.config import ADMINS

class IsAdminFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        # Implement your logic to check if the user is an admin
        # For example, you can check if the user ID is in a list of admin IDs
        admins = [123456789, 324234223]  # Example admin IDs
        return message.from_user.id in admins
