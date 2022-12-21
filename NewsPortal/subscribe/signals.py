from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Subscribe


@receiver(post_save, sender=Subscribe)
def successful_subscribe(sender, instance, created, **kwargs):
    if created:
        subject = f'You have subscribed for newsletters!'
    else:
        subject = f'You are subscriber already!'

    mail_managers(
        subject=subject,
        message=instance.message,
    )
