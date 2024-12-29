import logging
import re
from datetime import timedelta
from aiogram import types, Router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

group_router = Router()

BANNED_WORDS = {"spam", "zaza", "ad"}

def contains_banned_words(text: str) -> bool:
   if not text:
      return False
   words = set(re.findall(r"\w+", text.lower()))
   return not words.isdisjoint(BANNED_WORDS)

def parse_ban_duration(duration: str) -> timedelta:
   units = {
      "м": "minutes",
      "ч": "hours",
      "д": "days",
      "н": "weeks",
   }
   match = re.match(r"(\d+)([мчдн])", duration)
   if match:
      value, unit = match.groups()
      kwargs = {units[unit]: int(value)}
      return timedelta(**kwargs)
   raise ValueError("Некорректный формат времени")

@group_router.message()
async def check_banned_words(message: types.Message):
   if message.text and contains_banned_words(message.text):
      try:
         await message.chat.ban(user_id=message.from_user.id, until_date=timedelta(days=1))
         await message.delete()
         logger.info(f"Пользователь {message.from_user.id} забанен.")
      except Exception as e:
         logger.error(f"Ошибка при бане пользователя: {e}")