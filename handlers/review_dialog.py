from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from typing import Dict
import re
from keyboards.review import get_review_keyboard, get_food_rating_inline_keyboard, get_cleanliness_rating_inline_keyboard, get_extra_comments_keyboard
from config import database

class RestaurantReview(StatesGroup):
    waiting_for_name = State()
    waiting_for_contact = State()
    waiting_for_date = State()
    waiting_for_food_rating = State()
    waiting_for_cleanliness_rating = State()
    waiting_for_extra_comments = State()

review_router = Router()

user_reviews: Dict[int, Dict] = {}

@review_router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Добро пожаловать! Нажмите кнопку, чтобы оставить отзыв.", reply_markup=get_review_keyboard())

@review_router.callback_query(F.data == "review")
async def start_review(call: CallbackQuery, state: FSMContext) -> None:
    user_id = call.from_user.id
    if user_id in user_reviews:
        await call.message.answer("Вы уже оставили отзыв. Спасибо!")
        await state.clear()
        return
    await call.message.answer("Как вас зовут?")
    await state.set_state(RestaurantReview.waiting_for_name)

@review_router.message(RestaurantReview.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    name = message.text.strip()
    if not (2 <= len(name) <= 50):
        await message.answer("Имя должно содержать от 2 до 50 символов. Попробуйте снова.")
        return
    await state.update_data(name=name)
    await message.answer("Введите ваш номер телефона или ник в Instagram.")
    await state.set_state(RestaurantReview.waiting_for_contact)

@review_router.message(RestaurantReview.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext) -> None:
    contact = message.text.strip()
    if len(contact) < 5:
        await message.answer("Контактные данные слишком короткие. Попробуйте снова.")
        return
    await state.update_data(contact=contact)
    await message.answer("Когда вы посетили наше заведение? Укажите дату в формате ДД.ММ.ГГГГ.")
    await state.set_state(RestaurantReview.waiting_for_date)

@review_router.message(RestaurantReview.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext) -> None:
    date = message.text.strip()
    if not re.match(r"\d{2}\.\d{2}\.\d{4}", date):
        await message.answer("Дата должна быть в формате ДД.ММ.ГГГГ. Попробуйте снова.")
        return
    await state.update_data(date=date)
    await message.answer("Как вы оцениваете качество еды? (1 - плохо, 5 - отлично)", reply_markup=get_food_rating_inline_keyboard())
    await state.set_state(RestaurantReview.waiting_for_food_rating)

@review_router.callback_query(RestaurantReview.waiting_for_food_rating)
async def process_food_rating(call: CallbackQuery, state: FSMContext) -> None:
    if call.data not in {"1", "2", "3", "4", "5"}:
        await call.message.answer("Выберите оценку от 1 до 5.")
        return
    await state.update_data(food_rating=int(call.data))
    await call.message.answer("Как вы оцениваете чистоту заведения? (1 - плохо, 5 - отлично)", reply_markup=get_cleanliness_rating_inline_keyboard())
    await state.set_state(RestaurantReview.waiting_for_cleanliness_rating)

@review_router.callback_query(RestaurantReview.waiting_for_cleanliness_rating)
async def process_cleanliness_rating(call: CallbackQuery, state: FSMContext) -> None:
    if call.data not in {"1", "2", "3", "4", "5"}:
        await call.message.answer("Выберите оценку от 1 до 5.")
        return
    await state.update_data(cleanliness_rating=int(call.data))
    await call.message.answer("Добавьте дополнительные комментарии или выберите 'Пропустить'.", reply_markup=get_extra_comments_keyboard())
    await state.set_state(RestaurantReview.waiting_for_extra_comments)

@review_router.message(RestaurantReview.waiting_for_extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    extra_comment = message.text.lower() if message.text.lower() != "пропустить" else "Нет комментариев"

    user_reviews[message.from_user.id] = {
        "name": data["name"],
        "contact": data["contact"],
        "date": data["date"],
        "food_rating": data["food_rating"],
        "cleanliness_rating": data["cleanliness_rating"],
        "extra_comments": extra_comment,
    }
    
    database.save_poll(data)

    await message.answer(f"Спасибо, {data[name]}, за ваш отзыв! Мы ценим ваше мнение.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()