"""
WSGI config for timezup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timezup.settings')

application = get_wsgi_application()


# Setting background processes in wsgi.py bcz it is entry point for server and start our scheduler
# It's like we're setting cron-jobs django have cron-tab but that not work on windows
# so we instead using APScheduler 
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from tasks.cronjob_handlers import *
from django.conf import settings
# Creating scheduler instance to run in background
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE) # Setting timezone is important, default=UTC
scheduler.add_jobstore(DjangoJobStore(), "default") # 'default' alias for our scheduler which is DjangoJobStore
# Adding jobs in job store with their configuration
scheduler.add_job(send_daily_task_reminder_mail_morning, 
    trigger="cron", hour="8", minute="0", 
    id="morning_reminder", max_instances=1, replace_existing=True) # execute 08:00AM daily
scheduler.add_job(send_daily_task_reminder_mail_night, 
    trigger="cron", hour="21", minute="0", 
    id="night_reminder", max_instances=1, replace_existing=True) # execute 09:00PM daily

# Starting the scheduler in memory - jobs also stored in memory
scheduler.start()
