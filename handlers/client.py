from button.client_kb import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.admin import FSMAdmin
from create_bot import bot, ID
from info import course
from data_base.sql_db_admin import sql_read_command_admin
from data_base.sql_db_client import sql_add_command_client


class FSMClient(StatesGroup):
    full_price = State()
    numofpos = State()
    final_price = State()


FSMAdmin.get_root()
# @dp.callback_query_handler(text='price', state='*')
async def cb_price(callback: types.CallbackQuery, state : FSMContext):
    """Получение данных о заказе - ОБЩАЯ СТОИМОСТЬ"""
    price_kb = types.InlineKeyboardMarkup(row_width=1)
    price_kb.add(cancel, back)

    await state.update_data(IDmes=callback.message.message_id) # Записываем ID сообщения от нас
    await state.update_data(Name=callback.from_user.username)
    await state.update_data(URL=f'tg://user?id={callback.from_user.id}')
    await state.update_data(course=course)

    await state.set_state(FSMClient.full_price.state) # Переключаем состояние в 1 положение
    await callback.message.edit_text(f'[Введите общую стоимость заказа в CNY]',
                                     reply_markup=price_kb)


# @dp.callback_query_handler(text='отмена', state='*')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    """Сброс состояния"""
    cancel_kb = types.InlineKeyboardMarkup(row_width=1)
    cancel_kb.add(new, back)

    current_state = await state.get_state()
    if current_state is None:
        return
    await callback.answer(text='Данные удалены',show_alert=True)
    await state.finish()
    await callback.message.edit_text(text='Заказ очищен',reply_markup=cancel_kb)


# @dp.message_hendler(state=FSMClient.full_price)
async def quantity(message : types.Message, state : FSMContext):
    """Получение данных о заказе - КОЛИЧЕСТВО ТОВАРОВ"""
    quantity_kb = types.InlineKeyboardMarkup(row_width=1)
    quantity_kb.add(cancel, back)

    # print(message.from_user.id) # Получаем ID пользователя

    await state.update_data(FullPrice=message.text) # Записываем полную цену
    await message.delete() # Удаляем сообщение пользователя
    await FSMClient.next()

    user_data = await state.get_data()
    IDmes = user_data['IDmes'] # ID Прошлого сообщения от бота
    FullPrice = user_data['FullPrice'] # Общая цена заказа

    await bot.edit_message_text( #Изменяем сообщение отправленное нами до этого
                                chat_id=message.chat.id,
                                message_id=IDmes,
                                text=f'[Сколько всего позиций в заказе?\n'
                                     f'Общая цена: {FullPrice}]',
                                reply_markup=quantity_kb)


# @dp.message_hendler(state=FSMClient.numofpos)
async def calculation(message: types.Message, state: FSMContext):
    """Получение данных о заказе - ПОДТВЕРЖДЕНИЕ"""
    calculation_kb = types.InlineKeyboardMarkup(row_width=1)
    calculation_kb.add(cancel, go)

    await state.update_data(NumOfPos=message.text)
    await message.delete()
    await FSMClient.next()

    user_data = await state.get_data()
    IDmes = user_data['IDmes'] # ID Прошлого сообщения от бота
    FullPrice = user_data['FullPrice'] # Общая цена заказа
    NumOfPos = user_data['NumOfPos'] # Общее кол-во товаров
    records = sql_read_command_admin()

    await bot.edit_message_text( # Выводим всю информацию пользователю и просим подтвердить
                                 # отправку заказа Андрею.
                                chat_id=message.chat.id,
                                message_id=IDmes,
                                text=f'[Вы указали:\n'
                                     f'Стоимость : {FullPrice}\n'
                                     f'Кол-во : {NumOfPos}\n'
                                     f'Общая стоимость {round( (int(FullPrice) * course) + int(NumOfPos)*((records[0][1]+records[0][2])*course+records[0][3]),2)}руб.]',
                                reply_markup=calculation_kb)

# @dp.callback_query_handler(text='go', state='final_price')
async def cmd_okay(callback: types.CallbackQuery, state : FSMContext):
    """Отправляем заказ Андрею"""
    ok_kb = types.InlineKeyboardMarkup(row_width=1)
    ok_kb.add(back)


    user_data = await state.get_data()
    FullPrice = user_data['FullPrice'] # Общая цена заказа
    NumOfPos = user_data['NumOfPos'] # Общее кол-во товаров
    records = sql_read_command_admin()

    await state.update_data(Result=round( (int(FullPrice) * course) + int(NumOfPos)*((records[0][1]+records[0][2])*course+records[0][3]),2))
    await callback.answer(text='Заказ принят!', show_alert=True)
    await callback.message.edit_text(text='Ваш заказ принят!', reply_markup=ok_kb)
    await bot.send_message(chat_id=ID,
                           text=f'Стоимость : {FullPrice}\n'
                                f'Кол-во : {NumOfPos}\n'
                                f'Итоговая цена: {round( (int(FullPrice) * course) + int(NumOfPos)*((records[0][1]+records[0][2])*course+records[0][3]),2)}руб.\n'
                                f'[{callback.from_user.username}](tg://user?id={callback.from_user.id})',
                           )
    await sql_add_command_client(state)


def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(cb_price, text='price', state='*')
    dp.register_callback_query_handler(cancel_handler, text='отмена', state='*')

    dp.register_message_handler(quantity, state=FSMClient.full_price)
    dp.register_message_handler(calculation, state=FSMClient.numofpos)
    dp.register_callback_query_handler(cmd_okay, text='go', state=FSMClient.final_price)