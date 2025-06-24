import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from celery.signals import setup_logging

from django.conf import settings

logger = get_task_logger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TPV_public.settings')

app = Celery('TPV_public')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every hour.
    sender.add_periodic_task(
                                crontab(hour='*',minute=0), 
                                hourlyTasks.s('hello'), name='main hourly')

    # Executes everyday morning at 0:00 a.m.
    sender.add_periodic_task(
                                crontab(hour=0,minute=0), #hour=0, minute=0,
                                dailyTasks.s(),name='main daily')
    
    # Executes everyday morning at 0:00 a.m.
    sender.add_periodic_task(
                                crontab(month_of_year='*',day_of_month=1,hour=0,minute=0), #hour=0, minute=0,
                                monthlyTasks.s(),name='main monthly')
    
@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa
    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)
    
@app.task(name='main Hourly task')
def hourlyTasks(arg):
    import logging
    logger = logging.getLogger("celery")
    logger.info(arg)

@app.task(name='main Daily task')
def dailyTasks():
    import logging
    logger = logging.getLogger("celery")
    logger.info("Enters daily-task")
    os.system('sudo certbot renew --nginx')
    os.system('sudo systemctl restart nginx.service')
    logger.info("SSL Certificates renewal executed")

@app.task(name='main Monthly task')
def monthlyTasks():
    import logging
    logger = logging.getLogger("celery")
    logger.info("Enters monthly-task")
    