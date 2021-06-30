from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
import sys
# from celery.schedules import crontab
# from celery.tasks import periodic_task

# @periodic_task(run_every=crontab(seconds = 4))
# def every_monday_morning():
#     print("This is run every Monday morning at 7:30")

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def myjob():
    print('HALLOOOO !!')

class Scheduler:
    def start(self):
        job_defaults = {
            'coalesce': True,
        }
        self.scheduler = BackgroundScheduler(job_defaults=job_defaults)
        self.scheduler.add_jobstore(DjangoJobStore(), "default")
        # run this job every 24 hours
        trigger = IntervalTrigger(seconds=10)
        self.scheduler.add_job(myjob, trigger, name='clean_accounts', jobstore='default', max_instances=1, misfire_grace_time=2, id='job1', replace_existing=True)
        register_events(self.scheduler)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()
        print("Scheduler stopped...", file=sys.stdout)

