import logging
from datetime import datetime, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from news_portal.models import Category, Post

logger = logging.getLogger(__name__)


def my_job():
    # Your job processing logic here...
    emails = {}
    week_ago = datetime.now() - timedelta(days=7)
    url = 'http://127.0.0.1:8000'
    logger.info('starting job')

    for category in Category.objects.all():
        _category = category.cat_name.title()
        articles = Post.objects.filter(post_cat=category,
                                       post_pub_date__gte=week_ago)
        logger.info(f'found articles in {category}\n{articles}')
        if not articles:
            continue
        for user in category.subscribers.all():
            if user not in emails:
                emails[user] = {}
            if _category not in emails[user]:
                emails[user][_category] = set()
            emails[user][_category].update(articles)
    logger.info('sending mail', emails)

    for user, categories in emails.items():
        message = []
        for category, articles in categories.items():
            message.extend((category, *(
                f'{article.post_header}: {url}/{article.get_absolute_url()}'
                for article in articles)))
        send_mail('New articles of this week', '\n'.join(message), None,
                  [user.email])


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
