# Generated by Django 4.1.4 on 2022-12-23 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, max_length=50, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
