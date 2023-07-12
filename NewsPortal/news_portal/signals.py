from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from NewsPortal import settings
from news_portal.models import Post


@receiver(post_save, sender=Post)
def notify_update_subscribers(sender, instance, created, **kwargs):
    categories = instance.post_cat.all()
    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails = [user.email for user in subscribers]
        send_mail(
            subject=f'NEWSPORTAL. New publication!',
            message=f'There is new publication in your favorite category:\n\n'
                    f'{instance.post_text[:50]}...'
                    f'Follow the link:\n http://127.0.0.1:8000/{instance.get_absolute_url()}',
            from_email=settings.SERVER_EMAIL,
            recipient_list=subscribers_emails
        )
