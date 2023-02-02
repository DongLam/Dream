from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataBet.settings')
app = Celery('DataBet')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    # "crawler_bet_winner": {
    #     "task": "crawler.tasks.crawl_bet_winner",
    #     "schedule": crontab(minute='*/1')
    # },
    # "crawler": {
    #     "task": "crawler.tasks.crawl_bet_winner",
    #     "schedule": crontab(minute='*/1')
    # },
    # "detect_task": {
    #     "task": "crawler.tasks.detect_task",
    #     "schedule": crontab(minute='*/11')
    # },
    "crawl_task": {
        "task": "crawler.tasks.crawl_task",
        "schedule": crontab(minute='*/5')
    },
    # "send_notice": {
    #     "task": "crawler.tasks.send_notice_task",
    #     "schedule": crontab(minute='*/9')
    # },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))