from aiogram.types import InlineKeyboardButton

Delivery = InlineKeyboardButton('Стоимость доставки', callback_data='delivery')
Guarantee = InlineKeyboardButton('Стоимость гарантии', callback_data='guarantee')
Commission = InlineKeyboardButton('Комиссия', callback_data='commission')

Done = InlineKeyboardButton('Принять✅', callback_data='done')