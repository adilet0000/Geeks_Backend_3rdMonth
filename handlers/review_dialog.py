from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from typing import Dict
from keyboards.review import get_food_rating_keyboard, get_cleanliness_rating_keyboard

class RestaurantReview(StatesGroup):
    waiting_for_name = State()
    waiting_for_contact = State()
    waiting_for_food_rating = State()
    waiting_for_cleanliness_rating = State()
    waiting_for_extra_comments = State()

review_router = Router()

user_reviews: Dict[int, Dict] = {}

@review_router.callback_query()
async def start_review(call: CallbackQuery, state: FSMContext) -> None:
    if call.data != "review":
        return
    user_id = call.from_user.id
    if user_id in user_reviews:
        await call.message.answer("Вы уже оставили отзыв. Спасибо!")
        await state.clear()
        return
    await call.message.answer("Как вас зовут?")
    await state.set_state(RestaurantReview.waiting_for_name)

@review_router.message(RestaurantReview.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона или ник в Instagram.")
    await state.set_state(RestaurantReview.waiting_for_contact)

@review_router.message(RestaurantReview.waiting_for_contact)
async def process_contact(message: types.Message, state: FSMContext) -> None:
    contact = message.text
    if len(contact) < 5:
        await message.answer("Контактные данные слишком короткие. Попробуйте снова.")
        return
    
    await state.update_data(contact=contact)
    
    rating_kb = get_food_rating_keyboard()
    
    await message.answer("Как вы оцениваете качество еды? (1 - плохо, 5 - отлично)", reply_markup=rating_kb)
    await state.set_state(RestaurantReview.waiting_for_food_rating)

@review_router.message(RestaurantReview.waiting_for_food_rating)
async def process_food_rating(message: types.Message, state: FSMContext) -> None:
    if message.text not in {"1", "2", "3", "4", "5"}:
        await message.answer("Введите число от 1 до 5.")
        return
    await state.update_data(food_rating=int(message.text))
    
    rating_kb = get_cleanliness_rating_keyboard()
    
    await message.answer("Как вы оцениваете чистоту заведения? (1 - плохо, 5 - отлично)", reply_markup=rating_kb)
    await state.set_state(RestaurantReview.waiting_for_cleanliness_rating)

@review_router.message(RestaurantReview.waiting_for_cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext) -> None:
    if message.text not in {"1", "2", "3", "4", "5"}:
        await message.answer("Введите число от 1 до 5.")
        return
    await state.update_data(cleanliness_rating=int(message.text))
    
    await message.answer("Добавьте дополнительные комментарии или оставьте жалобу (Если хотите пропустить введите: '-').", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RestaurantReview.waiting_for_extra_comments)

@review_router.message(RestaurantReview.waiting_for_extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    
    extra_comment = message.text.lower() if message.text.lower() != "пропустить" else "Нет комментариев"
    
    user_reviews[message.from_user.id] = {
        "name": data["name"],
        "contact": data["contact"],
        "food_rating": data["food_rating"],
        "cleanliness_rating": data["cleanliness_rating"],
        "extra_comments": extra_comment,
    }

    await message.answer("Спасибо за ваш отзыв! Мы ценим ваше мнение.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


def get_review_keyboard() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review"))
    return kb
