from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


# Send verification mail to user
class TaskMail:
    def __init__(self, subject, to, from_email=None, 
        body =None, is_html=False, html_message=None, **kwargs):
        try:
            # Getting plain text messageif html messsage exist
            body = strip_tags(html_message) if not isinstance(html_message, None.__class__) else body

            # Creatin mail instance
            mail = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=to, **kwargs)

            # If html message exist setting it in email
            if is_html and not isinstance(html_message, None.__class__):
                mail.attach_alternative(html_message, "text/html")
                mail.content_subtype = "html"
            mail.send(fail_silently=False)
        except Exception as e:
            print(f"Development Error: Sending Email in mail.py - Subject: {subject}", e)