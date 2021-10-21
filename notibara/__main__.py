from pathlib import Path
from datetime import datetime as dt
import requests as r
import schedule as s
import pickle as p
import time
import os

GOTIFY_URL = os.environ.get('GOTIFY_URL')
GOTIFY_APP_TOKEN = os.environ.get('GOTIFY_APP_TOKEN')
PICKLE_PATH = Path('/storage/capy.p')
MIN_CAPYS = os.environ.get('MIN_CAPYS')


def push_notification(title, message):
    """Pushes notification to gotify server."""
    resp = r.post(
        'https://{}/message?token={}'.format(GOTIFY_URL, GOTIFY_APP_TOKEN),
        json={
            'message': message,
            'title': title,
            'priority': 2
        }
    )
    p.dump(dt.now(), open(PICKLE_PATH, 'wb'))


def job():
    if PICKLE_PATH.exists():
        last_notification = p.load(open(PICKLE_PATH, 'rb'))
        td = dt.now() - last_notification
        if td.seconds / (60 * 60) > 12:
            check_capys()


def check_capys():
    res = r.get('https://capybara.lol/api/stats')
    if res.status_code != 200:
        push_notification(
            'Network error!',
            'Could not reach capybara.lol'
        )
    else:
        resp_dict = res.json()
        n_capys = resp_dict.get('capybaras_enqueued')
        if n_capys and n_capys <= MIN_CAPYS:
            push_notification(
                'Low capybara queue',
                'only {} capybaras left'.format(n_capys)
            )
            


if __name__ == '__main__':

    s.every(10).minutes.do(check_capys)

    while True:
        s.run_pending()
        time.sleep(1)
