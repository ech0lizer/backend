from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['email_to']])
        email.send()

    @staticmethod
    def send_html_email(data):
        html_content = render_to_string(data['email_template'], data)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject=data['email_subject'], body=text_content, to=[data['email_to']])
        email.attach_alternative(html_content, 'text/html')
        email.send()
