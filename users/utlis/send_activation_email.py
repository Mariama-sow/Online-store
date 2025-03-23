from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

def send_activation_mail(user):
    subject = "Activation de compte"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    html_message = render_to_string(
        'registrations/activation_email.html', {
            'user': user,
            'uid': uid,
            'token': token,
            'domain': settings.DOMAIN_URL
        }
    )
    
    # Utiliser send_mail avec html_message comme paramètre nommé
    send_mail(
        subject=subject,
        message="",  # Message texte vide
        from_email='sowmariama2385@gmail.com',
        recipient_list=[user.email],
        html_message=html_message,  # Passer le HTML comme paramètre nommé
        fail_silently=False
    )