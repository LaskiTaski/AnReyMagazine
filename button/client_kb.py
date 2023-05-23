from aiogram.types import InlineKeyboardButton

price = InlineKeyboardButton('Рассчитать стоимость заказа🗑', callback_data='price')
new = InlineKeyboardButton('Расчитать заново🗑', callback_data='price')

cancel = InlineKeyboardButton('Отменить🙅‍♂', callback_data='отмена')

back = InlineKeyboardButton('Вернуться в меню🔙', callback_data='start')
go = InlineKeyboardButton('Всё верно! Отправить заказ✅', callback_data='go')

txt_one = InlineKeyboardButton('О приложении📂', callback_data='txt_one')
txt_two = InlineKeyboardButton('О составлении заказаℹ', callback_data='txt_two')