import logging
from celery import shared_task

from django.core.mail import send_mail
from core import settings


logger = logging.getLogger(__name__)


@shared_task
def send_email_async(title: str, email_body: str, recipient_list: list) -> None:

    send_mail(
        title,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        auth_user=settings.DEFAULT_FROM_EMAIL,
        auth_password=settings.EMAIL_HOST_PASSWORD,
    )
