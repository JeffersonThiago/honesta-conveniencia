import smtplib

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail




@shared_task(bind=True, autoretry_for=(smtplib.SMTPException,), retry_backoff=60, max_retries=3)
def send_email_async(self, title: str, email_body: str, recipient_list: list) -> None:
    try:
        send_mail(
            title,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            auth_user=settings.DEFAULT_FROM_EMAIL,
            auth_password=settings.EMAIL_HOST_PASSWORD,
        )

    except smtplib.SMTPRecipientsRefused:
        return f"Erro: Destinatário inválido {recipient_list}"

    except smtplib.SMTPException as e:
        raise self.retry(exc=e)