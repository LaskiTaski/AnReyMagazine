from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

currency = InlineKeyboardButton('Актуальный курс💹', callback_data='currency')
article_one = InlineKeyboardButton('О приложении📂', callback_data='article_one')
article_two = InlineKeyboardButton('О составлении заказаℹ', callback_data='article_two')
price = InlineKeyboardButton('Рассчитать стоимость заказа🗑', callback_data='price')


back = InlineKeyboardButton('Вернуться в меню🔙', callback_data='back_menu')
