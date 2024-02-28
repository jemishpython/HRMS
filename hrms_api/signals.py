from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template import loader
from hrms_api.models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        user_email = instance.email
        username = instance.username

        mail_subject = f"Welcome, {username}"

        context = {
            'username': username,
        }

        from_email = settings.EMAIL_HOST_USER
        email = loader.render_to_string('create_user_email_template.html', context)

        send_mail(
            subject=mail_subject,
            message=email,
            from_email=from_email,
            recipient_list=['pythonjemish.webmigrates@gmail.com',user_email],
            html_message=email,
            fail_silently=False,
        )
        return "mail sent"
