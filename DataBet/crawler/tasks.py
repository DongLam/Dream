from datetime import datetime

from celery import shared_task

from crawler.craw import egb, bet_winner, ps38, send_notice, sbotop, stake
from crawler.detect import detect, lam, detect_exception
from crawler.export import remove_data
from crawler.tele_bot import send_message
from crawler.views import get_data_bet_winner


@shared_task()
def crawl_egb():
    egb()

@shared_task()
def crawl_bet_winner():
    timeStamp = datetime.now()
    bet_winner(timeStamp)

@shared_task()
def crawl_task():
    print(111111111)
    remove_data()
    timeStamp = datetime.now()
    # egb(timeStamp)
    sbotop(timeStamp)
    bet_winner(timeStamp)
    stake(timeStamp)
    # ps38(timeStamp)
    # detect_exception()
    send_notice()

@shared_task()
def send_notice_task():
    send_notice()

@shared_task()
def detect_task():
    lam()

@shared_task()
def remove_data_task():
    remove_data()

