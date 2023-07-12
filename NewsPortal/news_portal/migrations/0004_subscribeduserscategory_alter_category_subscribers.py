# Generated by Django 4.1.4 on 2023-07-12 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_portal', '0003_alter_category_subscribers'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribedUsersCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.category')),
                ('subscribers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(through='news_portal.SubscribedUsersCategory', to=settings.AUTH_USER_MODEL),
        ),
    ]
