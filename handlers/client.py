from button.client_kb import *
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot


class FSMClient(StatesGroup):
    full_price_CNY = State()
    full_position = State()
    full_price_RUB = State()

# ЖДЁМ Ввод стоимости заказа в CNY
# @dp.callback_query_handler(text='price', state=None)
async def cb_price(callback: types.CallbackQuery, state : FSMContext):
    price_kb = types.InlineKeyboardMarkup(row_width=1)
    price_kb.add(cancel, back)
    await state.update_data(id_one=callback.message.message_id)
    await state.set_state(FSMClient.full_price_CNY.state)
    await callback.message.edit_text(f'[Введите Цену товара в CNY]',
                                     reply_markup=price_kb)


#Выход из состояний
# @dp.callback_query_handler(state='*', commands='отмена')
# @dp.callback_query_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    cancel_kb = types.InlineKeyboardMarkup(row_width=1)
    cancel_kb.add(cancel, back)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.answer(text='Данные удалены',show_alert=True)


# ЖДЁМ Кол-во позиций
# @dp.message_hendler(state=FSMClient.full_price_CNY)
async def quantity(message : types.Message, state : FSMContext):
    quantity_kb = types.InlineKeyboardMarkup(row_width=1)
    quantity_kb.add(cancel, back)
    await state.update_data(CNY_text=message.text)
    await message.delete()
    await FSMClient.next()
    await state.update_data(id_two=message.message_id)
    user_data = await state.get_data()
    id_one = user_data['id_one']
    CNY_text = user_data['CNY_text']
    await bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=id_one,
                                text=f'[А теперь введите кол-во позиций:\n'
                                     f'Цена товара: {CNY_text}]',
                                reply_markup=quantity_kb)


# # 22 доставка, 30 гарантия груза, 1000
# @dp.message_hendler(state=FSMClient.full_position)
async def calculation(message: types.Message, state: FSMContext):
    calculation_kb = types.InlineKeyboardMarkup(row_width=1)
    calculation_kb.add(cancel, back)

    await state.update_data(POS_text=message.text)

    await message.delete()
    await FSMClient.next()
    user_data = await state.get_data()
    id_two = user_data['id_two']
    POS_text = user_data['POS_text']
    await bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=id_two,
                                text=f'[А т\n'
                                     f'Цена товара: {POS_text}]',
                                reply_markup=calculation_kb)



def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(cb_price, text='price', state=None)
    dp.register_callback_query_handler(cancel_handler, state='*', text='отмена')
    dp.register_callback_query_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(quantity, state=FSMClient.full_price_CNY)
    dp.register_message_handler(calculation, state=FSMClient.full_position)


