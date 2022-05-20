import telegram

from crawler.constants import TELE_BOT_TOKEN, TELE_CHAT_ID


def send_message(message):
    try:
        telegram_notify = telegram.Bot(TELE_BOT_TOKEN)
        telegram_notify.send_message(chat_id=TELE_CHAT_ID, text=message,
                                     parse_mode='Markdown')
        print('1111111111111111111')
    except Exception as ex:
        print(ex)