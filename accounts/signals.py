from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.tasks import send_email_async
from .models import User


@receiver(post_save, sender=User)
def send_verification_code_email(sender, instance, created, **kwargs):
    if created:
        title = "[HONESTA CONVENIÊNCIA] - Código de verificação"
        body = f"""
        Olá {instance.first_name} {instance.last_name},

        Bem-vindo ao nosso site. Estamos felizes por você ter se juntado a nós!

        Segue abaixo o código para ativação da conta:
        
        {instance.verification_code}
        
        Atenciosamente,
        
        Equipe Honesta Conveniência.
        """
        recipient_email = [instance.email]
        send_email_async.apply_async(args=[title, body, recipient_email])
