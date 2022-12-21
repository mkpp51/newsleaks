from django.apps import AppConfig


class SubscribeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscribe'

    # def ready(self):
    #     import subscribe.signals
    #
    #     from .tasks import send_mails
    #     from .scheduler import subscribe_scheduler
    #     print('started')
    #
    #     subscribe_scheduler.add_job(
    #         id='send mails',
    #         func=lambda: print('Mail!'),
    #         trigger='interval',
    #         seconds=10,
    #     )
    #
    #     subscribe_scheduler.start()
