from django.conf import settings
from tasks.helper_methods import send_reminder_mail


# In morning send mail to all user for their daily tasks
def send_daily_task_reminder_mail_morning():
    subject_greet = "Good Morning"
    small_message = f"Welcome the new day with a smile, armed with the confidence that you can \
tick off the goals you've set in {settings.PROJECT_APPLICATION_NAME}. Get ready for something \
amazing to unfold – it's the sweet taste of accomplishment waiting for you!"
    send_reminder_mail(subject_greet, small_message)

send_daily_task_reminder_mail_morning()