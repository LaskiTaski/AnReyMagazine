from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import ID, bot
from button.admin_kb import *


class FSMAdmin(StatesGroup):
    Admin = State()


# @dp.message_handler( commands=['esmin'], state='*' )
async def cmd_admin(message: types.Message, state: FSMContext):
    """Запуск админских настроек"""
    if ID == message.from_user.id:
        admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
        admin_menu_kb.add(Delivery, Guarantee, Commission)

        await state.set_state(FSMAdmin.Admin.state)
        await message.answer(f'[Что меняем?]',
                             reply_markup=admin_menu_kb)


# @dp.callback_query_handler( text=delivery, state=FSMAdmin.Admin )
async def cb_dtlivery(callback: types.CallbackQuery, state: FSMContext):
    """Изменение стоимости доставки"""
    admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    admin_menu_kb.add(Delivery, Guarantee, Commission)

    await state.update_data(IDA=callback.message.message_id)  # Записываем ID сообщения от нас
    await callback.message.edit_text(f'[Какая будет стоимость заказа?]',
                                     reply_markup=admin_menu_kb)


# @dp.message_handler( text=delivery, state=FSMAdmin.Admin )
async def quantity(message: types.Message, state: FSMContext):
    """Изменение стоимости гарантии"""
    admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    admin_menu_kb.add(Delivery, Guarantee, Commission)

    await state.update_data(delivery=message.text)  # Записываем стоимость доставки
    await message.delete()  # Удаляем сообщение пользователя
    await FSMAdmin.next()

    user_data = await state.get_data()
    ID = user_data['ID']  # ID Прошлого сообщения от бота
    delivery = user_data['delivery']  # Цена за доставку

    await bot.edit_message_text(  # Изменяем сообщение отправленное нами до этого
        chat_id=message.chat.id,
        message_id=ID,
        text=f'Готово! Что-то ещё?'
             f'Цена за доставку сейчас {delivery}',
        reply_markup=admin_menu_kb)

