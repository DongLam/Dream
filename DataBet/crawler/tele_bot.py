import telegram

from crawler.constants import TELE_BOT_TOKEN, TELE_CHAT_ID, TELE_CHAT_ID_2


def send_message(message):
    try:
        telegram_notify = telegram.Bot(TELE_BOT_TOKEN)
        telegram_notify.send_message(chat_id=TELE_CHAT_ID, text=message,
                                     parse_mode='Markdown')
        print('1111111111111111111')
    except Exception as ex:
        print(ex)

def send_message_bo2(message):
    try:
        telegram_notify = telegram.Bot(TELE_BOT_TOKEN)
        telegram_notify.send_message(chat_id=TELE_CHAT_ID_2, text=message,
                                     parse_mode='Markdown')
        print('2222222222222222')
    except Exception as ex:
        print(ex)