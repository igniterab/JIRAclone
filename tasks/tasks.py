from celery import shared_task
from django.core.mail import send_mail
from jira import settings

@shared_task(bind=True)
def send_mail_func(self, receipent_email, receipent_name):
    #This function is used in order to send email to the team leader, in case a task is created.
    #"robin@frejun.com"
    mail_subject = f"Hello {receipent_name} - Task created"
    message = f"Heyy {receipent_name} a new task has been created for your team " \
        "please check your JIRA on time."
    
    to_email=receipent_email

    send_mail(
        subject= mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )