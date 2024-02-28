import time
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def add(a: int, b: int) -> int:
    return a + b


@shared_task
def send_email_task(recipient: str, subject: str, message: str):
    time.sleep(5)
    return send_mail(
        subject, message, "proguser111@gmail.com", [recipient], fail_silently=False
    )
