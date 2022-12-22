from django.core.mail import send_mail
from django.template.loader import render_to_string

msg_plain = render_to_string('subscribe/subscribed.txt')
msg_html = render_to_string('subscribe/subscribed.html')


def send(user_email):
    send_mail(
        'NewsPortal - Successful subscription',
        msg_plain,
        'fam.ilya51@yandex.ru',
        [user_email],
        html_message=msg_html,
    )
