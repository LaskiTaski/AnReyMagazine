from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import ID, bot
from button.admin_kb import *
from data_base import sql_db_admin


class FSMAdmin(StatesGroup):
    Admin = State()
    Done = State()
    Delivery = State()
    Delivery_done = State()
    Guarantee = State()
    Guarantee_done = State()
    Commission = State()
    Commission_done = State()


# @dp.message_handler( commands=['esmin'], state='*' )
async def cmd_admin(message: types.Message, state: FSMContext):
    """Запуск админских настроек"""
    if int(ID) == int(message.from_user.id):
        admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
        admin_menu_kb.add(Delivery, Guarantee, Commission)

        async with state.proxy() as data:
                data['id'] = 1
                data['delivery'] = 24
                data['guarantee'] = 40
                data['commission'] = 1000

        await  sql_db_admin.sql_add_command_admin(state)
        records = sql_db_admin.sql_read_command_admin()
        await FSMAdmin.Admin.set()
        await message.answer(f'Что меняем?\n'
                             f'Расценки сейчас:\n'
                             f'Доставка: {records[0][1]}\n'
                             f'Гарантия: {records[0][2]}\n'
                             f'Комиссия: {records[0][3]}',
                             reply_markup=admin_menu_kb)


# @dp.callback_query_handler( text='done', state=(FSMAdmin.Delivery_done, FSMAdmin.Guarantee_done, FSMAdmin.Commission_done) )
async def cmd_done(callback: types.CallbackQuery, state: FSMContext):
    """Запуск админских настроек"""
    admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    admin_menu_kb.add(Delivery, Guarantee, Commission)

    records = sql_db_admin.sql_read_command_admin()
    await FSMAdmin.Admin.set()
    await callback.message.edit_text(
                                text=f'Что меняем?\n'
                                     f'Расценки сейчас:\n'
                                     f'Доставка: {records[0][1]}\n'
                                     f'Гарантия: {records[0][2]}\n'
                                     f'Комиссия: {records[0][3]}',
                                reply_markup=admin_menu_kb)


# @dp.callback_query_handler( text='delivery', state=FSMAdmin.Admin )
async def cb_delivery(callback: types.CallbackQuery, state: FSMContext):
    """Изменение стоимости доставки"""

    await FSMAdmin.Delivery.set()

    await state.update_data(IDA=callback.message.message_id)  # Записываем ID сообщения от нас
    await callback.message.edit_text(f'[Какая будет стоимость заказа?]')


# @dp.message_handler( state=FSMAdmin.Delivery )
async def cb_delivery_done(message: types.Message, state: FSMContext):
    """Применение изм. доставки"""
    admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    admin_menu_kb.add(Done)

    await state.update_data(delivery=message.text)  # Записываем стоимость доставки
    await message.delete()  # Удаляем сообщение пользователя
    await FSMAdmin.Delivery_done.set()

    user_data = await state.get_data()
    IDA = user_data['IDA']  # ID Прошлого сообщения от бота
    delivery = user_data['delivery']  # Цена за доставку
    await sql_db_admin.sql_update_command_admin('Delivery',delivery)

    await bot.edit_message_text(  # Изменяем сообщение отправленное нами до этого
        chat_id=message.chat.id,
        message_id=IDA,
        text=f'Готово! Что-то ещё?'
             f'Цена за доставку сейчас {delivery}',
        reply_markup=admin_menu_kb)


# @dp.callback_query_handler( text='guarantee', state=FSMAdmin.Admin )
async def cb_guarantee(callback: types.CallbackQuery, state: FSMContext):
    """Изменение стоимости гарантии"""

    await FSMAdmin.Guarantee.set()

    await state.update_data(IDA=callback.message.message_id)  # Записываем ID сообщения от нас
    await callback.message.edit_text(f'[Какую установить стоимость гарантии?]')


# @dp.message_handler( state=FSMAdmin.Guarantee )
async def cb_guarantee_done(message: types.Message, state: FSMContext):
    """Применение изм. гарантии"""
    admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    admin_menu_kb.add(Done)

    await state.update_data(guarantee=message.text)
    await message.delete()
    await FSMAdmin.Guarantee_done.set()

    user_data = await state.get_data()
    IDA = user_data['IDA']  # ID Прошлого сообщения от бота
    guarantee = user_data['guarantee']  # Цена за доставку
    await sql_db_admin.sql_update_command_admin('Guarantee', guarantee)

    await bot.edit_message_text(  # Изменяем сообщение отправленное нами до этого
        chat_id=message.chat.id,
        message_id=IDA,
        text=f'Готово! Что-то ещё?'
             f'Цена гарантии сейчас {guarantee}',
        reply_markup=admin_menu_kb)


# @dp.callback_query_handler( text='commission', state=FSMAdmin.Admin )
async def cb_commission(callback: types.CallbackQuery, state: FSMContext):
    """Изменение стоимости комиссии"""

    await FSMAdmin.Commission.set()

    await state.update_data(IDA=callback.message.message_id)  # Записываем ID сообщения от нас
    await callback.message.edit_text(f'[Какую установить стоимость комиссии?]')


# @dp.message_handler( state=FSMAdmin.Commission )
async def cb_commission_done(message: types.Message, state: FSMContext):
    """Применение изм. комиссии"""
    admin_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    admin_menu_kb.add(Done)

    await state.update_data(commission=message.text)
    await message.delete()
    await FSMAdmin.Commission_done.set()

    user_data = await state.get_data()
    IDA = user_data['IDA']  # ID Прошлого сообщения от бота
    commission = user_data['commission']  # Цена за доставку
    await sql_db_admin.sql_update_command_admin('Commission', commission)

    await bot.edit_message_text(  # Изменяем сообщение отправленное нами до этого
        chat_id=message.chat.id,
        message_id=IDA,
        text=f'Готово! Что-то ещё?'
             f'Цена комиссии сейчас {commission}',
        reply_markup=admin_menu_kb)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_admin, commands=['esmin'], state='*')
    dp.register_callback_query_handler(cmd_done, text='done', state=(FSMAdmin.Delivery_done,
                                                                     FSMAdmin.Guarantee_done,
                                                                     FSMAdmin.Commission_done)
                                       )
    dp.register_callback_query_handler(cb_delivery, text='delivery', state=FSMAdmin.Admin)
    dp.register_message_handler(cb_delivery_done, state=FSMAdmin.Delivery)

    dp.register_callback_query_handler(cb_guarantee, text='guarantee', state=FSMAdmin.Admin)
    dp.register_message_handler(cb_guarantee_done, state=FSMAdmin.Guarantee)

    dp.register_callback_query_handler(cb_commission, text='commission', state=FSMAdmin.Admin)
    dp.register_message_handler(cb_commission_done, state=FSMAdmin.Commission)
