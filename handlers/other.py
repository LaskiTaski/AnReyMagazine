from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from button.other_kb import *
from info import course
from handlers.client import FSMClient


# @dp.message_handler( commands=['start'], state = '*' )
async def cmd_start( message : types.Message, state : FSMContext ):

    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( price, txt_one, txt_two )

    await state.set_state(FSMClient.full_price.state)

    await message.answer(f'[Информация о ЧЁМ-ТО\n](https://telegra.ph/Informaciya-o-magazine-05-07)'
                         f'Актуальный курс:\n'
                         f'1 Китайский юань = {float(course)} Российского рубля',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='start', state = '*')
async def cb_menu(callback: types.CallbackQuery):
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( price, txt_one, txt_two )
    await callback.message.edit_text(f'[Информация о ЧЁМ-ТО\n](https://telegra.ph/Informaciya-o-magazine-05-07)'
                         f'Актуальный курс:\n'
                         f'1 Китайский юань = {float(course)} Российского рубля',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='txt_one', state='*')
async def cb_txt_one(callback: types.CallbackQuery):
    txt_kb = types.InlineKeyboardMarkup(row_width=1)
    txt_kb.add( back )
    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №1]'
                                     f'(https://telegra.ph/O-prilozhenii-05-07)',
                                     reply_markup=txt_kb)


# @dp.callback_query_handler(text='txt_two', state='*')
async def cb_txt_two(callback: types.CallbackQuery):
    txt_kb = types.InlineKeyboardMarkup(row_width=1)
    txt_kb.add( back )
    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №2]'
                                     f'(https://telegra.ph/O-sovershenii-zakaza-05-07)',
                                     reply_markup=txt_kb)


def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands='start', state='*')
    dp.register_callback_query_handler(cb_menu, text='start', state='*')
    dp.register_callback_query_handler(cb_txt_one, text='txt_one', state='*')
    dp.register_callback_query_handler(cb_txt_two, text='txt_two', state='*')