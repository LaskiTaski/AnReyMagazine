from aiogram.types import InlineKeyboardButton

price = InlineKeyboardButton('Рассчитать стоимость заказа🗑', callback_data='price')
new = InlineKeyboardButton('Нажмите, чтобы начать заново🗑', callback_data='price')

back = InlineKeyboardButton('Вернуться в меню🔙', callback_data='back_menu')
cancel = InlineKeyboardButton('Отменить🙅‍♂', callback_data='отмена')
