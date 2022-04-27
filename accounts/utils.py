from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from .models import Account

def send_verification_email(request, user_id):
    user = Account.objects.get(id=user_id)
    if user.is_active:
        messages.success(request, 'Your account is already active. Just Sign In.')
        return redirect('sign_in')
    current_site = get_current_site(request)
    mail_subject = 'Link To Activate Your Account'
    message = render_to_string('registration/verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    return redirect('sign_in')