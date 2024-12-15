from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_review_keyboard() -> ReplyKeyboardMarkup:
   return ReplyKeyboardMarkup(
      keyboard=[
         [KeyboardButton(text="Оставить отзыв")],
      ],
      resize_keyboard=True,
      one_time_keyboard=True
   )

def get_review_keyboard() -> InlineKeyboardMarkup:
   return InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="Оставить отзыв", callback_data="review")]
   ])


def get_food_rating_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data="1"), InlineKeyboardButton(text="2", callback_data="2")],
            [InlineKeyboardButton(text="3", callback_data="3"), InlineKeyboardButton(text="4", callback_data="4")],
            [InlineKeyboardButton(text="5", callback_data="5")],
        ]
    )

def get_cleanliness_rating_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data="1"), InlineKeyboardButton(text="2", callback_data="2")],
            [InlineKeyboardButton(text="3", callback_data="3"), InlineKeyboardButton(text="4", callback_data="4")],
            [InlineKeyboardButton(text="5", callback_data="5")],
        ]
    )


def get_extra_comments_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Пропустить")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
