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
    await state.update_data(ID=callback.message.message_id)
    await state.set_state(FSMClient.full_price_CNY.state)
    await callback.message.edit_text(f'[Введите Цену товара в CNY]',
                                     reply_markup=price_kb)


#Выход из состояний
# @dp.callback_query_handler(text='отмена', state='*')
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    cancel_kb = types.InlineKeyboardMarkup(row_width=1)
    cancel_kb.add(new, back)

    current_state = await state.get_state()
    if current_state is None:
        return
    await callback.answer(text='Данные удалены',show_alert=True)
    await callback.message.edit_text(text='Данные удалены',reply_markup=cancel_kb)
    await state.finish()


# ЖДЁМ Кол-во позиций
# @dp.message_hendler(state=FSMClient.full_price_CNY)
async def quantity(message : types.Message, state : FSMContext):
    quantity_kb = types.InlineKeyboardMarkup(row_width=1)
    quantity_kb.add(cancel, back)

    await state.update_data(CNY=message.text)
    await message.delete()
    await FSMClient.next()
    user_data = await state.get_data()
    ID = user_data['ID']
    CNY = user_data['CNY']
    await bot.edit_message_text(
                                chat_id=message.chat.id,
                                message_id=ID,
                                text=f'[А теперь введите кол-во позиций:\n'
                                     f'Цена товара: {CNY}]',
                                reply_markup=quantity_kb)


# # 22 доставка, 30 гарантия груза, 1000
# @dp.message_hendler(state=FSMClient.full_position)
async def calculation(message: types.Message, state: FSMContext):
    calculation_kb = types.InlineKeyboardMarkup(row_width=1)
    calculation_kb.add(cancel, back)

    await state.update_data(POS=message.text)
    current = message.chat.id
    await message.delete()
    await FSMClient.next()
    user_data = await state.get_data()
    ID = user_data['ID']
    CNY = user_data['CNY']
    POS = user_data['POS']
    await bot.edit_message_text(
                                chat_id=current,
                                message_id=ID,
                                text=f'[Вы указали:\n'
                                     f'Стоимость : {CNY}\n'
                                     f'Кол-во : {POS}\n'
                                     f'Общая стоимость {int(CNY)*int(POS)}]',
                                reply_markup=calculation_kb)
# (цена+22+30 * кол-во позиций)*курс + (кол-поз*1000)

def register_handlers_client(dp : Dispatcher):
    dp.register_callback_query_handler(cb_price, text='price', state=None)
    dp.register_callback_query_handler(cancel_handler, text='отмена', state='*')
    dp.register_message_handler(quantity, state=FSMClient.full_price_CNY)
    dp.register_message_handler(calculation, state=FSMClient.full_position)


