from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_mail_task(subject, body, sender, list_of_receivers):
    mail = send_mail(subject, body, sender, list_of_receivers, fail_silently=False)
    return mail
