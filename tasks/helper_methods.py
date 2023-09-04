from django.http import Http404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from .mail import TaskMail
from django.db.models import Q
from .models import Year, Month, Date
import hashlib
import threading
import datetime


# Validate aceepted year value
def validateYear(year):
    """
    Ensure that given year is in database

    Args: 
        year (int): Year
    Return:
        int: valid year else raise Http404
    """
    try:
        if isinstance(year, None.__class__):
            # If no year value than current year
            rec_year = int(datetime.datetime.now().strftime('%Y'))
            return rec_year
        else:
            # either given value map to id or data
            rec_year = Year.objects.get(data=year)
            return rec_year.data
    except Exception:
        raise Http404("Development: Invalid Year")
    

# Validate aceepted month value
def validateMonth(month):
    """
    Ensure that given month is valid month name or number

    Args: 
        month (int) | (str): month name or number
    Return:
        dict: Dictionary with two keys number and name of month else raise Http404
    """
    try:
        if not month.isdigit():
            month_id = None # if not numeric month then search primary key as null value
        else:
            month_id = month

        # either given value map to id or data
        rec_month = Month.objects.get(Q(pk=month_id) | Q(data=month))
        return {"number": rec_month.pk, "name": rec_month.data}
    except Exception:
        raise Http404(f"Development: Invalid Month")
    

# Validate aceepted date value
def validateDate(date : int, month : int, year : int):
    """
    Ensure that given date is validated based on month and year

    Args: 
        date (int): date
        month (int): month number
        year (int): year
    Returns:
        int: validated date base on given month and year
    """
    try:
        end_date = get_month_end_date(month, year)
        # either given value map to id or data
        rec_date = Date.objects.get(Q(data=date) & Q(data__lte=end_date))
        return rec_date.data
    except Exception:
        raise Http404("Development: Invalid Date")
    

# On the basis of month and year it return end date of that month
def get_month_end_date(month : int, year: int) -> int:
    """
    Get the end date for a month based on month and year

    Args: 
        month (int): month number
        year (int): year
    Returns:
        int: end date of month
    """
    # If its february only
    if month % 2 == 0 and month == 2:
        # if its a february of leap year
        if year % 4 == 0:
            end = 29
        else:
            end = 28
    elif month % 2 == 0 and month <= 7:
        end = 30
    elif month % 2 == 0 and (month > 7 and month <= 12):
        end = 31
    elif month % 2 != 0 and (month > 7 and month <= 12):
        end = 30
    else:
        end = 31
    return end


# Generate a hashed token for user
def generate_user_token(user) -> str:
    hash_core_data = str(user.id) + user.username + str(user.id) + user.email + str(user.id) + str(user.password[-10:])
    # This hash cannot be decoded
    hashed_token = hashlib.md5(hash_core_data.encode("utf-8")).hexdigest()

    ## Note ##
    # This token is same for email but if it is generated for password change then after
    # successful password change this token is not longer valid because user.password have different value
    # So for password change this token is one time use only 
    return hashed_token


# Generate uidb64 user id with expiry time
def urlsafe_base64_encode_with_expiry(user) -> str:
    # Setting expiration time for token
    expiry_time_in_second = int(datetime.datetime.timestamp(datetime.datetime.now())) + settings.TOKEN_EXPIRY_TIME
    user_id_and_expiry_time = str(user.id) + ":" + str(expiry_time_in_second)

    # This can be decoded while md5 only be encoded and compared with encoded
    hashed_user_id = urlsafe_base64_encode(user_id_and_expiry_time.encode("utf-8"))
    return hashed_user_id


# Decode uidb64 of user id and expiry time and return them in tuple
def urlsafe_base64_decode_with_expiry(uidb64) -> tuple:
    user_id_and_expiry_time = urlsafe_base64_decode(uidb64).decode("utf-8")
    user_id, expiry_time = user_id_and_expiry_time.split(":")
    return (user_id, expiry_time)


# Send user verification email
def send_mail_user_verify(user, is_forgot_password=False):
    if is_forgot_password:
        email_label_message = "Password change request accepted. Please click the button below \
to verify your email address and follow further instructioins"
        url_name = "tasks:url-forgot-password-verify"
    else:
        email_label_message = \
            "Thank you for choosing us. Please click the button below to verify your email address."
        url_name = "tasks:url-register-email-verify"
    # This hash cannot be decoded
    hashed_token = generate_user_token(user)

    # This can be decoded
    hashed_user_id = urlsafe_base64_encode_with_expiry(user)

    context = dict()
    context["app_name"] = settings.PROJECT_APPLICATION_NAME
    context["hashed_param"] = hashed_token
    context["hashed_id"] = hashed_user_id
    context["username"] = user.username
    context["domain"] = settings.DOMAIN
    context["email_label_message"] = email_label_message
    context["url_name"] = url_name
    message_html_format = \
        render_to_string("tasks/mail/email_confirmation.html", context)
    
    # Sending email confirmation link
    mail_thread = threading.Thread(target=TaskMail, 
        kwargs={"subject": f"{settings.PROJECT_APPLICATION_NAME} - Email Verification",
        "from_email": f"{settings.PROJECT_APPLICATION_NAME} <noreply@gmail.com>",
        "to": (user.email,), "is_html": True, "html_message": message_html_format})
    mail_thread.start()