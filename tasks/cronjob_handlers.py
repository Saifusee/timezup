from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from tasks.models import CombineDate, Date, Month, Year
from tasks.mail import TaskMail
import datetime
import threading


# In morning send mail to all user for their daily tasks
def send_daily_task_reminder_mail_morning():
    subject_greet = "Good Morning"
    small_message = f"Welcome the new day with a smile, armed with the confidence that you can \
tick off the goals you've set in {settings.PROJECT_APPLICATION_NAME}. Get ready for something \
amazing to unfold – it's the sweet taste of accomplishment waiting for you!"
    send_reminder_mail(subject_greet, small_message)
    

# In evening send mail to all user for their daily tasks
def send_daily_task_reminder_mail_night():
    subject_greet = "Good Evening"
    small_message = f"Reflecting on today's milestones, here's to hoping you conquered your goals! \
Now, let's pave the path for another victorious day with {settings.PROJECT_APPLICATION_NAME}. \
What will tomorrow bring? Let's make it extraordinary."
    send_reminder_mail(subject_greet, small_message)


def send_reminder_mail(subject_greet, small_message):
    # Getting today's date in integer
    todays_date = datetime.datetime.now()
    date = Date.objects.get(data=int(todays_date.day))
    month = Month.objects.get(pk=int(todays_date.month))
    year = Year.objects.get(data=int(todays_date.year))
    # CombineDate object of today's date
    combine_date, _ = CombineDate.objects.get_or_create(date=date, month=month, year=year)

    from_email = f"{settings.PROJECT_APPLICATION_NAME} <noreply@gmail.com>"
    subject = f"{settings.PROJECT_APPLICATION_NAME} - Today's Time Table"

    # In my opinion select_related for forward relationship and for reverse use prefetch_related
    users = get_user_model().objects.filter(is_active=True).prefetch_related("task_set")

    for user in users:
        context = {
            "app_name": settings.PROJECT_APPLICATION_NAME,
            "subject_greet": subject_greet,
            "username": user.username,
            "small_message": small_message,
            "tasks": user.task_set.filter(combine_date=combine_date)
        }
        html_message = render_to_string("tasks/mail/reminder_mail.html", context)
        mail_thread = threading.Thread(target=TaskMail, 
            kwargs={"subject": subject,
            "from_email": from_email,
            "to": (user.email,), "is_html": True, "html_message": html_message})
        mail_thread.start()