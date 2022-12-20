from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post


class PostFilter(FilterSet):
    post_header = CharFilter(
        'post_header',
        label='Contains words in header:',
        lookup_expr='icontains',
    )

    post_text = CharFilter(
        'post_text',
        label='Contains words text:',
        lookup_expr='icontains',
    )

    datetime = DateFilter(
        field_name='post_pub_date',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='After the date:'
    )

    class Meta:
        model = Post
        fields = []
