from aiogram import types, Dispatcher
from button.other_kb import *
from info import currency_info


# @dp.message_handler( commands=['start'] )
async def cmd_start( message : types.Message ):
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( currency, article_one, article_two )
    await message.answer(f'[Информация о ЧЁМ-ТО](https://telegra.ph/Informaciya-o-magazine-05-07)',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='back_menu')
async def cb_back_menu(callback: types.CallbackQuery):
    start_menu_kb = types.InlineKeyboardMarkup(row_width=1)
    start_menu_kb.add( currency, article_one, article_two )
    await callback.message.edit_text(f'[Информация о ЧЁМ-ТО](https://telegra.ph/Informaciya-o-magazine-05-07)',
                         reply_markup=start_menu_kb)


# @dp.callback_query_handler(text='currency')
async def cb_currency(callback: types.CallbackQuery):
    currency_kb = types.InlineKeyboardMarkup(row_width=1)
    currency_kb.add( price, back )
    await callback.message.edit_text(f'[Курс сейчас\n{currency_info()}]'
                                     f'(https://telegra.ph/Kakoj-sejchas-kurs-CNY--RUB-05-07)',
                                     reply_markup=currency_kb)

# @dp.callback_query_handler(text='article_one')
async def cb_article_one(callback: types.CallbackQuery):
    article_kb = types.InlineKeyboardMarkup(row_width=1)
    article_kb.add( back )
    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №1]'
                                     f'(https://telegra.ph/O-prilozhenii-05-07)',
                                     reply_markup=article_kb)

# @dp.callback_query_handler(text='article_two')
async def cb_article_two(callback: types.CallbackQuery):
    article_kb = types.InlineKeyboardMarkup(row_width=1)
    article_kb.add( back )
    await callback.message.edit_text(f'[ТВОЙ ТЕКСТ №2]'
                                     f'(https://telegra.ph/O-sovershenii-zakaza-05-07)',
                                     reply_markup=article_kb)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_callback_query_handler(cb_back_menu, text='back_menu')
    dp.register_callback_query_handler(cb_currency, text='currency')
    dp.register_callback_query_handler(cb_article_one, text='article_one')
    dp.register_callback_query_handler(cb_article_two, text='article_two')