import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random_recipe import random_recipe_router
from handlers.review_dialog import review_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(myinfo_router)
dp.include_router(random_recipe_router)
dp.include_router(review_router)

async def main():
   print("\nБот запущен!\n")
   await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())
# ВОПРОС ПО ШИФТ_АЛЬТ_Ф