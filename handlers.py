from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import *
from aiogram.filters import Text

from config import PAYMENT_TOKEN

router = Router()


@router.message(Command(commands=['start']))
async def startCommand(message: Message):
    pay_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить', callback_data='pay-data')]
    ])
    await message.answer('Для оплаты нажмите на кнопку', reply_markup=pay_keyboard)


@router.callback_query(Text(text='pay-data'))
async def pay_button_click(call: CallbackQuery, bot: Bot):
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title='Оплата занятия',
        description='Перевод средств за 1 час занятия',
        # Служебная информация, которая может понадобиться программисту и не видна для пользователя
        payload='123456',
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        #
        prices=[
            LabeledPrice(label='Стоимость занятия', amount=3000),
            LabeledPrice(label='Скидка', amount=-500),
            LabeledPrice(label='Покупка JetBrains', amount=2000)
        ],
        # Максимальный размер чаевых ???????????????????????????????????????
        max_tip_amount=1000,
        # Значения чаевых на выбор
        suggested_tip_amounts=[100, 200, 500, 1000],
        # Информация, которую может требовать платёжный провайдер
        provider_data=None,
        # Ссылка на картинку, которая будет отображаться при оплате
        photo_url='https://fb.ru/media/i/1/0/6/3/7/3/7/i/1063737.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=400,
        # Параметры, обязывающие пользователя вводить соответствующие значения
        need_name=True,
        need_email=True,
        need_phone_number=True,
        # Попробовать !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        need_shipping_address=False,
        # Параметры отправки платёжному провайдеру информации о покупателе
        send_email_to_provider=False,
        send_phone_number_to_provider=False
    )


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_types == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await message.answer('Оплата прошла успешно!')
