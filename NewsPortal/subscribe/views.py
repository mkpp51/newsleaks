from django.core.mail import send_mail, mail_managers
from django.views.generic import CreateView

from .models import Subscribe
from .forms import SubscribeForm




class SubscribeView(CreateView):
    model = Subscribe
    form_class = SubscribeForm
    success_url = '/'


send_mail(
    'Successful subscription',
    'Congratulations! You have subscribed for the newsletters!',
    'fam.ilya51@yandex.ru',
    ['morjakpapaj51@gmail.com'],
    fail_silently=False,
)
