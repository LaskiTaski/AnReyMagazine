from button.client_kb import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot
from info import course

class FSMClient(StatesGroup):
    full_price = State()
    numofpos = State()
    final_price = State()


# @dp.message_handler( commands=['start'], state='*' )
async def cmd_start( message : types.Message, state : FSMContext ):
    """Запуск бота по команде start"""
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( price, txt_one, txt_two )
    print(message.from_user.id)

    await state.set_state(FSMClient.full_price.state)
    await message.answer(f'[Информация о ЧЁМ-ТО\n](https://telegra.ph/Informaciya-o-magazine-05-07)'
                         f'Актуальный курс:\n'
                         f'1 Китайский юань = {float(course)} Российского рубля',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='start', state='*' )
async def cb_menu(callback: types.CallbackQuery, state : FSMContext):
    """Возвращение в главное меню"""
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( price, txt_one, txt_two )

    await state.set_state(FSMClient.full_price.state)
    await callback.message.edit_text(f'[Информация о ЧЁМ-ТО\n](https://telegra.ph/Informaciya-o-magazine-05-07)'
                         f'Актуальный курс:\n'
                         f'1 Китайский юань = {float(course)} Российского рубля',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='txt_one', state='*' )
async def cb_txt_one(callback: types.CallbackQuery):
    """Текст о приложении (ТЕКСТ 1)"""
    txt_kb = types.InlineKeyboardMarkup(row_width=1)
    txt_kb.add( back )

    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №1]'
                                     f'(https://telegra.ph/O-prilozhenii-05-07)',
                                     reply_markup=txt_kb)


# @dp.callback_query_handler(text='txt_two', state='*' )
async def cb_txt_two(callback: types.CallbackQuery):
    """Текст о составлении заказа (ТЕКСТ 2)"""
    txt_kb = types.InlineKeyboardMarkup(row_width=1)
    txt_kb.add( back )

    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №2]'
                                     f'(https://telegra.ph/O-sovershenii-zakaza-05-07)',
                                     reply_markup=txt_kb)


# @dp.callback_query_handler(text='price', state='*')
async def cb_price(callback: types.CallbackQuery, state : FSMContext):
    """Получение данных о заказе - ОБЩАЯ СТОИМОСТЬ"""
    price_kb = types.InlineKeyboardMarkup(row_width=1)
    price_kb.add(cancel, back)

    await state.update_data(ID=callback.message.message_id) # Записываем ID сообщения от нас
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

    print(message.from_user.id) # Получаем ID пользователя

    await state.update_data(FullPrice=message.text) # Записываем полную цену
    await message.delete() # Удаляем сообщение пользователя
    await FSMClient.next()

    user_data = await state.get_data()
    ID = user_data['ID'] # ID Прошлого сообщения от бота
    FullPrice = user_data['FullPrice'] # Общая цена заказа

    await bot.edit_message_text( #Изменяем сообщение отправленное нами до этого
                                chat_id=message.chat.id,
                                message_id=ID,
                                text=f'[Сколько всего позиций в заказе?\n'
                                     f'Общая цена: {FullPrice}]',
                                reply_markup=quantity_kb)


# @dp.message_hendler(state=FSMClient.numofpos)
async def calculation(message: types.Message, state: FSMContext):
    """Получение данных о заказе - ПОДТВЕРЖДЕНИЕ"""
    calculation_kb = types.InlineKeyboardMarkup(row_width=1)
    calculation_kb.add(cancel, go)

    await state.update_data(NumOfPos=message.text) # Записываем кол-во позиций
    await message.delete()
    await FSMClient.next()

    user_data = await state.get_data()
    ID = user_data['ID'] # ID Прошлого сообщения от бота
    FullPrice = user_data['FullPrice'] # Общая цена заказа
    NumOfPos = user_data['NumOfPos'] # Общее кол-во товаров

    await bot.edit_message_text( # Выводим всю информацию пользователю и просим подтвердить
                                 # отправку заказа Андрею.
                                chat_id=message.chat.id,
                                message_id=ID,
                                text=f'[Вы указали:\n'
                                     f'Стоимость : {FullPrice}\n'
                                     f'Кол-во : {NumOfPos}\n'
                                     f'Общая стоимость {round( (int(FullPrice) * course) + int(NumOfPos)*((24+40)*course+1000),2)}руб.]',
                                reply_markup=calculation_kb)

# @dp.callback_query_handler(text='go', state='final_price')
async def cmd_okay(callback: types.CallbackQuery, state : FSMContext):
    """Отправляем заказ Андрею"""
    ok_kb = types.InlineKeyboardMarkup(row_width=1)
    ok_kb.add(back)
    print('ЗАКАЗ ОТПРАВЛЕН')

    user_data = await state.get_data()
    FullPrice = user_data['FullPrice'] # Общая цена заказа
    NumOfPos = user_data['NumOfPos'] # Общее кол-во товаров

    await callback.answer(text='Заказ принят!', show_alert=True)
    await callback.message.edit_text(text='Ваш заказ принят!', reply_markup=ok_kb)
    await bot.send_message(chat_id=,
                           text=f'Стоимость : {FullPrice}\n'
                                f'Кол-во : {NumOfPos}\n'
                                f'Итоговая цена: {round( (int(FullPrice) * course) + int(NumOfPos)*((24+40)*course+1000),2)}руб.\n'
                                f'[{callback.from_user.username}](tg://user?id={callback.from_user.id})',
                           )


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*') #Меню START
    dp.register_callback_query_handler(cb_menu, text='start', state='*') #Меню Back
    dp.register_callback_query_handler(cb_txt_one, text='txt_one', state='*' ) #Текст 1
    dp.register_callback_query_handler(cb_txt_two, text='txt_two', state='*' ) #Текст 2

    dp.register_callback_query_handler(cb_price, text='price', state='*')
    dp.register_callback_query_handler(cancel_handler, text='отмена', state='*')

    dp.register_message_handler(quantity, state=FSMClient.full_price)
    dp.register_message_handler(calculation, state=FSMClient.numofpos)
    dp.register_callback_query_handler(cmd_okay, text='go', state=FSMClient.final_price)




