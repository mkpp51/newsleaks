from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail

from NewsPortal import settings
from news_portal.models import Post, Category


@shared_task
def notification_sender(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_cat.all()
    subscribers_emails = []
    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            subscribers_emails.append(user.email)

    send_mail(
        subject=f'NEWSPORTAL. New publication!',
        message=f'There is new publication in your favorite category:\n'
                f'{post.post_header}'
                f'{post.post_text[:100]}...\n'
                f'http://127.0.0.1:8000/news_portal/{pk}',
        from_email=settings.SERVER_EMAIL,
        recipient_list=subscribers_emails
    )


@shared_task
def weekly_updates_sender():
    subscribers_emails = []
    articles_list = []
    week_ago = datetime.now() - timedelta(days=7)

    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        _category = category.cat_name.title()
        articles = Post.objects.filter(post_cat=category,
                                       post_pub_date__gte=week_ago)
        articles_list.append(articles)
        for user in subscribers:
            subscribers_emails.append(user.email)

    send_mail(
        subject=f'NEWSPORTAL. Weekly publications compilation.',
        message=f'Weekly update on publication(s) in your favorite category(ies):\n'
                f'{articles_list}',
        from_email=settings.SERVER_EMAIL,
        recipient_list=subscribers_emails
    )
