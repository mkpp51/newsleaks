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
    emails = {}
    week_ago = datetime.now() - timedelta(days=7)
    url = 'http://127.0.0.1:8000'

    for category in Category.objects.all():
        _category = category.cat_name.title()
        articles = Post.objects.filter(post_cat=category,
                                       post_pub_date__gte=week_ago)
        if not articles:
            continue
        for user in category.subscribers.all():
            if user not in emails:
                emails[user] = {}
            if _category not in emails[user]:
                emails[user][_category] = set()
            emails[user][_category].update(articles)

    for user, categories in emails.items():
        message = []
        for category, articles in categories.items():
            message.extend((category, *(
                f'{article.post_header}: {url}/{article.get_absolute_url()}'
                for article in articles)))

        send_mail('New articles of this week', '\n'.join(message), None,
                  [user.email])
