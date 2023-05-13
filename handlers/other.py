from aiogram import types, Dispatcher
from button.other_kb import *
from info import data


# @dp.message_handler( commands=['start'] )
async def cmd_start( message : types.Message ):
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( price, txt_one, txt_two )
    await message.answer(f'[Информация о ЧЁМ-ТО\n](https://telegra.ph/Informaciya-o-magazine-05-07)'
                         f'Актуальный курс:\n'
                         f'1 Китайский юань = {float(data)} Российского рубля',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='menu')
async def cb_menu(callback: types.CallbackQuery):
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( price, txt_one, txt_two )
    await callback.message.edit_text(f'[Информация о ЧЁМ-ТО\n](https://telegra.ph/Informaciya-o-magazine-05-07)'
                         f'Актуальный курс:\n'
                         f'1 Китайский юань = {float(data)} Российского рубля',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='txt_one')
async def cb_txt_one(callback: types.CallbackQuery):
    txt_kb = types.InlineKeyboardMarkup(row_width=1)
    txt_kb.add( back )
    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №1]'
                                     f'(https://telegra.ph/O-prilozhenii-05-07)',
                                     reply_markup=txt_kb)


# @dp.callback_query_handler(text='txt_two')
async def cb_txt_two(callback: types.CallbackQuery):
    txt_kb = types.InlineKeyboardMarkup(row_width=1)
    txt_kb.add( back )
    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №2]'
                                     f'(https://telegra.ph/O-sovershenii-zakaza-05-07)',
                                     reply_markup=txt_kb)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_callback_query_handler(cb_menu, text='menu', state='*')
    dp.register_callback_query_handler(cb_txt_one, text='txt_one')
    dp.register_callback_query_handler(cb_txt_two, text='txt_two')