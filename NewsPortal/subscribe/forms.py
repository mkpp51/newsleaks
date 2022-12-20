from django import forms

from .models import Subscribe


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ('email', )
        widgets = {
            'email': forms.TextInput(attrs={'class': 'editContent', 'placeholder': 'Your e-mail...'})
        }
        labels = {
            'email': '',
        }
