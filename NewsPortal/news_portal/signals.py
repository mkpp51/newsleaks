from django.core.mail import send_mail
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from NewsPortal import settings
from news_portal.models import Post


@receiver(m2m_changed, sender=Post.post_cat.through)
def notify_update_subscribers(sender, instance, action, **kwargs):

    post_url = f'http://127.0.0.1:8000/{instance.get_absolute_url()}'
    categories = instance.post_cat.all()
    subscribers_emails = []
    for category in categories:
        subscribers = category.subscribers.all()
        subscribers_emails = [user.email for user in subscribers]

    if action == 'post_add':
        send_mail(
            subject=f'NEWSPORTAL. New publication! from signals',
            message=f'There is new publication in your favorite category:\n'
                    f'{instance.post_header}'
                    f'{instance.post_text[:100]}...\n'
                    f'Follow the link: {post_url}',
            from_email=settings.SERVER_EMAIL,
            recipient_list=subscribers_emails
        )

