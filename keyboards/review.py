from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_review_keyboard() -> InlineKeyboardMarkup:
   return InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="Оставить отзыв", callback_data="review")]
   ])


def get_food_rating_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для оценки качества еды"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3"), KeyboardButton(text="4"), KeyboardButton(text="5")]
        ],
        resize_keyboard=True
    )

def get_cleanliness_rating_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для оценки чистоты заведения"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1"), KeyboardButton(text="2"), KeyboardButton(text="3"), KeyboardButton(text="4"), KeyboardButton(text="5")]
        ],
        resize_keyboard=True
    )

def get_extra_comments_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Пропустить")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
