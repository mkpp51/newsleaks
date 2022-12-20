from django.views.generic import CreateView

from .models import Subscribe
from .forms import SubscribeForm


class SubscribeView(CreateView):
    model = Subscribe
    form_class = SubscribeForm
    success_url = '/'

