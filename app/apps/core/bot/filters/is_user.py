from aiogram import types
from aiogram.filters import Filter

from app.apps.core.bot.data.config import ADMINS


class IsUserFilter(Filter):
    async def check(self, message: types.Message):
        # Replace with your own logic to determine if the user is a regular user
        user_id = message.from_user.id
        return user_id not in ADMINS
    
    