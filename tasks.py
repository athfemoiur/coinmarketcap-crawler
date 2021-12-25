from celery import Celery
from celery.schedules import crontab

from crawler import CurrencyCrawler

app = Celery()
app.conf.beat_schedule = {
    'crawl': {
        'task': 'tasks.crawl',
        'schedule': crontab(minute='*/1'),
    },
}
app.conf.timezone = 'Asia/Tehran'


@app.task
def crawl():
    CurrencyCrawler(['BTC', 'ETH', 'BNB', 'USDT', 'SOL', 'USDC']).start()
