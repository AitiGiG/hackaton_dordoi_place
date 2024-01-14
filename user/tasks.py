from django.core.mail import send_mail
from celery import shared_task

from .models import User

@shared_task
def send_activation_email(email, activate_link):
    user = User.objects.get(email=email)
    subject = 'Activate your account'
    message = f'Please use the link to activate your account: {activate_link}'
    from_email = 'fitstreety@gmail.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome!',
        'Welcome to our site!',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )

@shared_task
def send_password_reset_email(email, reset_link):
    subject = 'Reset your password'
    message = f'Please use the link to reset your password: {reset_link}'
    from_email = 'fitstreety@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)