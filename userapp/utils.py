from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random

def generate_scheme_and_domain(request):
    return [request.scheme, request.get_host()]

def send_email_via_template(subject, recipient_list, template_name, context):
    from_email = settings.EMAIL_HOST_USER
    
    html_content = render_to_string(template_name, context)
    
    text_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    
    email.attach_alternative(html_content, "text/html")
    
    return email.send()

def generateOtp():
    otp=""
    for i in range(6):
        otp+=str(random.randint(0,9))
    return otp


# def send_code_to_user(email):
#     Subject="One time passcode for Email verification"
#     otp_code=generateOtp()
#     user=User.objects.get(email=email)
#     current_site="sparkle.sync"
#     front_end_url = f"{settings.FRONT_END_URL}/verify_email"
#     email_body=f"Hello {user.first_name} thank you for signing up on {current_site} please visit {front_end_url} to verify your email with the following \n one time passcode {otp_code}"
#     from_email=settings.DEFAULT_FROM_EMAIL
    
#     OneTimePassword.objects.create(user=user, code=otp_code)
    
#     d_email= EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
#     d_email.send(fail_silently=True)
    
def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send(fail_silently=True)