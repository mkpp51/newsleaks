from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    post_text = forms.CharField(min_length=100)

    class Meta:
        model = Post
        fields = [
            'post_header',
            'post_text',
            'post_cat',
            'post_auth'
        ]

    def clean(self):
        cleaned_data = super().clean()
        post_header = cleaned_data.get("post_header")
        post_text = cleaned_data.get("post_text")

        if post_header == post_text:
            raise ValidationError(
                "Header and text couldn't be the same."
            )

        return cleaned_data
