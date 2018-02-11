from __future__ import absolute_import, unicode_literals
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task, current_task
from celery.schedules import crontab
from celery.task import periodic_task


@shared_task
def create_random_user_accounts(total_user):
    for i in range(total_user):
        username = 'user_%s' % get_random_string(20, string.ascii_letters)
        email = '%s@example.com' % username
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
        current_task.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': total_user,
                                        'percent': int((float(i) / total_user) * 100)})
    return {'current': total_user, 'total': total_user, 'percent': 100}


@shared_task
def add(a, b):
    print(a + b)


@shared_task
def mul(a, b):
    print(a * b)


@periodic_task(run_every=(crontab(minute='*/1')), name="task-hello")
def print_hello():
    print('Hello World!')
