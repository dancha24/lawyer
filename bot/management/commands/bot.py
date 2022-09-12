import telebot
from telebot import types
from bot import names
from telebot.types import LabeledPrice, PreCheckoutQuery
import requests
from bot.models import Botset
from django.core.management.base import BaseCommand



# Создаем экземпляр бота
bot = telebot.TeleBot(Botset.objects.get(pk=1).set)
paytok = Botset.objects.get(pk=2).set
starttext = Botset.objects.get(pk=3).set
if Botset.objects.get(pk=4).set == 'Да':
    paytg = False
else:
    paytg = True

markuponeper = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("В начало")
markuponeper.add(item1)

markuponeper = types.ReplyKeyboardMarkup(resize_keyboard=True)


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **options):

        import requests
        from bot.models import Promocodes
        # Получение сообщений от юзера
        @bot.pre_checkout_query_handler(func=lambda query: True)
        def checkout(pre_checkout_query):
            bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                          error_message="Оплата не прошла - попробуйте, пожалуйста, еще раз,"
                                                        "или свяжитесь с администратором бота.")

        # Команда start
        @bot.message_handler(commands=["start"])
        def start(m, res=False):
            # Добавляем две кнопки
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # item1 = types.KeyboardButton("Есть промомкод")
            # item2 = types.KeyboardButton("Продолжить без промокода")
            # markup.add(item1)
            # markup.add(item2)
            # bot.send_message(m.chat.id, 'У вас есть промокод? ', reply_markup=markup)
            # Добавляем две кнопки
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Подключение к сервису")
            item2 = types.KeyboardButton("Ежемесячная абонентская плата")
            item3 = types.KeyboardButton("Связаться с нами")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(m.chat.id, starttext, reply_markup=markup)

        @bot.message_handler(content_types=['successful_payment'])
        def got_payment(message):
            bot.send_message(message.chat.id,
                             'Ура!\n'
                             'Оплата прошла успешно'.format(
                                 message.successful_payment.total_amount / 100, message.successful_payment.currency),
                             parse_mode='Markdown')
            suma = str(message.successful_payment.total_amount / 100)
            username = message.from_user.username
            # lidname = 'Оплата VPN ' + message.from_user.username
            nameall = message.from_user.first_name + ' ' + message.from_user.last_name
            # name = message.from_user.first_name
            # last_name = message.from_user.last_name
            # phone = message.from_user.phone_number
            r = requests.get(
                'https://avtopark.bitrix24.ru/crm/configs/import/lead.php?LOGIN=dancha241@gmail.com&PASSWORD=03081998'
                '&TITLE=Оплата%20с%20телеграма'
                '&NAME=' + nameall + '&COMMENTS=коментарий'
                                     '&PHONE_MOBILE=89236034317'
                                     '&SOURCE_ID=Телеграм%20покер'
                                     '&UF_CRM_1585304121=Покер%20IT'
                                     '&ASSIGNED_BY_ID=1836'
                                     '&OPPORTUNITY=' + suma)

        # Получение сообщений от юзера
        @bot.message_handler(content_types=["text"])
        def handle_text(message):
            if message.text == 'В начало':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Подключение к сервису")
                item2 = types.KeyboardButton("Ежемесячная абонентская плата")
                item3 = types.KeyboardButton("Связаться с нами")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                bot.send_message(message.chat.id, starttext, reply_markup=markup)
                return True

            if message.text == 'Оплата подключения к сервису':
                bot.send_message(message.chat.id,
                                 'Оплачива вы соглашаетесь с условием использовния https://xn--b1aaeeocmc7adp0a2e.xn--p1ai/ispolsovanie',
                                 reply_markup=markuponeper)
                bot.send_message(message.chat.id,
                                 'По независящим от нас причинам, при оплате картами банка происходит ошибка. '
                                 'Стабильно работает оплата через кошелек Юмани и SberPay. '
                                 'Мы работаем над увеличением количества способов оплаты.')
                # bot.send_invoice(chat_id=message.chat.id, title='Оплата', description='Описание оплаты',
                #                  invoice_payload='papay', provider_token=names.kassatoken, currency='RUB',
                #                  start_parameter='test', prices=[LabeledPrice(label='Working Time Machine', amount=200000)])
                bot.send_message(message.chat.id, 'Ссылка на оплату: https://inlnk.ru/meMJlG')
                return True

            if message.text == '1 месяц - 1000р':
                bot.send_message(message.chat.id,
                                 'Оплачива вы соглашаетесь с условием использовния https://xn--b1aaeeocmc7adp0a2e.xn--p1ai/ispolsovanie',
                                 reply_markup=markuponeper)
                # bot.send_invoice(chat_id=message.chat.id, title='Оплата', description='Описание оплаты',
                #                  invoice_payload='papay', provider_token=paytok, currency='RUB',
                #                  start_parameter='test', prices=[LabeledPrice(label='Working Time Machine', amount=1000000)])
                bot.send_message(message.chat.id, 'Ссылка на оплату: https://inlnk.ru/zaOYA5')
                return True

            if message.text == '3 месяца - 2700р':
                bot.send_message(message.chat.id,
                                 'Оплачива вы соглашаетесь с условием использовния https://xn--b1aaeeocmc7adp0a2e.xn--p1ai/ispolsovanie',
                                 reply_markup=markuponeper)
                bot.send_message(message.chat.id,
                                 'По независящим от нас причинам, при оплате картами банка происходит ошибка. '
                                 'Стабильно работает оплата через кошелек Юмани и SberPay. '
                                 'Мы работаем над увеличением количества способов оплаты.')
                # bot.send_invoice(chat_id=message.chat.id, title='Оплата', description='Описание оплаты',
                #                  invoice_payload='papay', provider_token=paytok, currency='RUB',
                #                  start_parameter='test', prices=[LabeledPrice(label='Working Time Machine', amount=270000)])
                bot.send_message(message.chat.id, 'Ссылка на оплату: https://inlnk.ru/ELjG1g')

                return True

            if message.text == '6 месяцев - 5000р':
                bot.send_message(message.chat.id,
                                 'Оплачива вы соглашаетесь с условием использовния https://xn--b1aaeeocmc7adp0a2e.xn--p1ai/ispolsovanie',
                                 reply_markup=markuponeper)
                bot.send_message(message.chat.id,
                                 'По независящим от нас причинам, при оплате картами банка происходит ошибка. '
                                 'Стабильно работает оплата через кошелек Юмани и SberPay. '
                                 'Мы работаем над увеличением количества способов оплаты.')
                # bot.send_invoice(chat_id=message.chat.id, title='Оплата', description='Описание оплаты',
                #                  invoice_payload='papay', provider_token=paytok, currency='RUB',
                #                  start_parameter='test', prices=[LabeledPrice(label='Working Time Machine', amount=500000)])
                bot.send_message(message.chat.id, 'Ссылка на оплату: https://inlnk.ru/l0KlJn')
                return True

            if message.text == '1 год - 9000р':
                bot.send_message(message.chat.id,
                                 'Оплачива вы соглашаетесь с условием использовния https://xn--b1aaeeocmc7adp0a2e.xn--p1ai/ispolsovanie',
                                 reply_markup=markuponeper)
                bot.send_message(message.chat.id,
                                 'По независящим от нас причинам, при оплате картами банка происходит ошибка. '
                                 'Стабильно работает оплата через кошелек Юмани и SberPay. '
                                 'Мы работаем над увеличением количества способов оплаты.')
                # bot.send_invoice(chat_id=message.chat.id, title='Оплата', description='Описание оплаты',
                #                  invoice_payload='papay', provider_token=paytok, currency='RUB',
                #                  start_parameter='test', prices=[LabeledPrice(label='Working Time Machine', amount=900000)])
                bot.send_message(message.chat.id, 'Ссылка на оплату: https://inlnk.ru/NDNPR2')

                return True

            if message.text == 'Подключение к сервису':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item2 = types.KeyboardButton("Оплата подключения к сервису")
                item1 = types.KeyboardButton("Оплата подключения к сервису с промокодом")
                item3 = types.KeyboardButton("В начало")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                bot.send_message(message.chat.id, 'Варианты оплаты ', reply_markup=markup)
                return True

            if message.text == 'Ежемесячная абонентская плата':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("1 месяц - 1000р")
                item2 = types.KeyboardButton("3 месяца - 2700р")
                item3 = types.KeyboardButton("6 месяцев - 5000р")
                item4 = types.KeyboardButton("1 год - 9000р")
                item5 = types.KeyboardButton("В начало")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)
                markup.add(item5)
                bot.send_message(message.chat.id, 'Варианты оплаты ', reply_markup=markup)
                return True

            if message.text == 'Оплата подключения к сервису с промокодом':
                bot.send_message(message.chat.id, 'Введите промокод учитывая регистр', reply_markup=markuponeper)
                return True
            if message.text == 'Связаться с нами':
                bot.send_message(message.chat.id,
                                 'Связаться с нами можно с помощью этого бота t.me/Comebackstarssupport_bot',
                                 reply_markup=markuponeper)
                return True

            if Promocodes.objects.filter(name=message.text.lower()).exists():
                prom = Promocodes.objects.get(name=message.text.lower())
                if prom.aktive:
                    bot.send_message(message.chat.id,
                                     'Оплачива вы соглашаетесь с условием использовния https://xn--b1aaeeocmc7adp0a2e.xn--p1ai/ispolsovanie',
                                     reply_markup=markuponeper)
                    bot.send_message(message.chat.id,
                                     'По независящим от нас причинам, при оплате картами банка происходит ошибка. '
                                     'Стабильно работает оплата через кошелек Юмани и SberPay. '
                                     'Мы работаем над увеличением количества способов оплаты.')
                    text = 'Ссылка на оплату: ' + prom.linkpay
                    bot.send_message(message.chat.id, text)
                else:
                    bot.send_message(message.chat.id, 'Промокод не действителен', reply_markup=markuponeper)
            else:
                bot.send_message(message.chat.id, 'Такого промокода не существует', reply_markup=markuponeper)

                # bot.send_invoice(chat_id=message.chat.id, title='Оплата2', description='Описание оплаты2',
                #                  invoice_payload='papay2', provider_token=paytok, currency='RUB',
                #                  start_parameter='test2', prices=[LabeledPrice(label='Working Time Machine2', amount=150000)])


        # Запускаем бота
        bot.polling(none_stop=True, interval=0)

