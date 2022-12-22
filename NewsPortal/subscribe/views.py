from django.views.generic import CreateView

from .models import Subscribe
from .forms import SubscribeForm
from .service import send


class SubscribeView(CreateView):
    model = Subscribe
    form_class = SubscribeForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        send(form.instance.email)
        return super().form_valid(form)



