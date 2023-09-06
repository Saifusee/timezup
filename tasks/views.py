from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.contrib.auth.views import LogoutView
from django.contrib.auth import get_user_model, authenticate, login
from django.conf import settings
from django.db.models import Q
from .models import CombineDate, Task, Year, Month, Date
from .forms import TaskForm, LoginForm, RegisterForm, PasswordChangeRequestForm, PasswordChangeConfirmForm
from .helper_methods import *
import datetime


# return error template
def viewRenderErrorTemplate(request):
    """
    Return error template as response
    Args: 
        request (django.http.request.HttpRequest)
    Returns:
        HttpResponse: an http response instance from render()
    """
    context = dict()
    context["app_name"] = settings.PROJECT_APPLICATION_NAME
    return render(request, "tasks/error.html", context)


# Index first page , months rendering
def viewIndex(request, year=None):
    year = validateYear(year)
    months_data = Month.objects.all()

    context = {
        'year': year,
        'months_data': months_data,
        'app_name': settings.PROJECT_APPLICATION_NAME,
        'username': request.user.username,
        'is_staff': request.user.is_staff

    }
    return render(request, 'tasks/index.html', context)


# Select year
def viewSelectYear(request):
    current_year = int(datetime.datetime.now().strftime('%Y'))
    context = {
        'current_year': current_year,
        'app_name': settings.PROJECT_APPLICATION_NAME,
        'username': request.user.username,
        'is_staff': request.user.is_staff
    }
    return render(request, 'tasks/years.html', context)


# Month wise dates rendering
def viewShowMonthDates(request, year, month):
    
    year = validateYear(year)
    month = validateMonth(month)
    end = get_month_end_date(month["number"], year)

    context = {
        'app_name': settings.PROJECT_APPLICATION_NAME,
        'year': year,
        'month_name': month["name"],
        'end_date': end,
        'username': request.user.username,
        'is_staff': request.user.is_staff
    }
    return render(request, 'tasks/month_dates.html', context)


# Date wise data show
def viewShowDateData(request, year, month, date):
    year = validateYear(year)
    month = validateMonth(month)
    date = validateDate(date, month['number'], year)
    
    year_inst = Year.objects.get(data=year)
    month_inst = Month.objects.get(pk=month["number"])
    date_inst = Date.objects.get(data=date)

    # since get_or_create return (object, created)
    combine_date, _ = CombineDate.objects.get_or_create(year=year_inst, month=month_inst, date=date_inst)
    tasks = Task.objects.filter(combine_date=combine_date, user=request.user)
    context = {
        'app_name': settings.PROJECT_APPLICATION_NAME,
        'year': year,
        'month': month["name"],
        'date': date,
        'tasks': tasks,
        'username': request.user.username,
        'is_staff': request.user.is_staff
    }

    return render(request, 'tasks/dates.html', context)


# Class based view for new Task Creation
# Replacing CreateView with FormView works same 
class ViewCreateTask(CreateView):
    template_name = "tasks/form.html"
    model = Task
    form_class = TaskForm
    success_mssg_ = ["Task successfully added"] # This is custom property
    # in context "form" already pass to form.html
    # If we want additional override with get_context_data

    # Ensuring date, month and year is valid
    def get(self, request, *args, **kwargs):
        year = validateYear(kwargs["year"])
        month = validateMonth(kwargs["month"])
        validateDate(kwargs["date"], month['number'], year)
        self.kwargs["month"] = month["name"] # if month no. in url then proceed with name 
        return super().get(request, *args, **kwargs)

    # Setting context for template rendering
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["date"] = self.kwargs["date"]
        context["month"] = self.kwargs["month"]
        context["year"] = self.kwargs["year"]
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["username"] = self.request.user.username
        context["is_staff"] = self.request.user.is_staff
        context["title"] = "Create Task"
        context["messages"] = self.success_mssg_
        context["show_message"] = False
        context["is_error"] = False
        context["submit_url"] = reverse_lazy("tasks:url-create-task", kwargs={
            "date": self.kwargs["date"],
            "month": self.kwargs["month"],
            "year": self.kwargs["year"]
            })
        month_no = int(validateMonth(self.kwargs["month"])["number"])
        requested_date = datetime.datetime(int(context["year"]), month_no, int(context["date"])).date()
        current_date = datetime.datetime.now().date()
        print(requested_date)
        print(current_date)
        if requested_date < current_date:
            context["form_not_accepted"] = True
        else:
            context["form_not_accepted"] = False
        return context
    
    # This method called when a valid form is submitted
    def form_valid(self, form):
        try:
            context = self.get_context_data()
            date = Date.objects.get(data=self.kwargs["date"])
            month = Month.objects.get(data=self.kwargs["month"])
            year = Year.objects.get(data=self.kwargs["year"])
            # get_or_create return tuple (object, boolean), boolean tell either new obj craeted or not
            combine_date, _ = CombineDate.objects.get_or_create(date=date, month=month, year=year)

            new_task = Task(task=form.cleaned_data["task"], combine_date=combine_date, 
                user=self.request.user)
            new_task.save()
            context["show_message"] = True # Show message
            context["is_error"] = False # There are no errors
            context["messages"] = self.success_mssg_
            return render(self.request, self.template_name, context)
        except Exception as e:
            print("Develoment Error: Creating Task :", e)
            # If Unique Constraint fail for duplicate entry on same date
            if "unique_task_date" in str(e):
                form.errors["custom_error"] = ["Task already exist for this date"]
                return self.form_invalid(form)
            else:
                form.errors["custom_error"] = ["Something went wrong, please try again later"]
                return self.form_invalid(form)
        
    # This method is called when a invalid form is submitted
    def form_invalid(self, form):
        context = self.get_context_data()
        context["show_message"] = True # Show message
        context["is_error"] = True # There are errors
        context["messages"] = [error for field_errors in form.errors.values()
                                for error in field_errors] # Flattening Dict of fields(keys): errors (list) 
        return render(self.request, self.template_name, context)
    

# Class based view for updation of Task
class ViewEditTask(UpdateView):
    template_name = "tasks/form.html"
    model = Task
    form_class = TaskForm
    success_mssg_ = ["Task modified successfully"]
    # in context "form" already pass to form.html
    # If we want additional override with get_context_data

    # Setting context for template rendering
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        combined_date = self.get_object().combine_date
        context["date"] = combined_date.date.data
        context["month"] = combined_date.month.data
        context["year"] = combined_date.year.data
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["username"] = self.request.user.username
        context["is_staff"] = self.request.user.is_staff
        context["title"] = "Edit Task"
        context["messages"] = self.success_mssg_
        context["show_message"] = False
        context["is_error"] = False
        context["submit_url"] = reverse_lazy("tasks:url-edit-task", kwargs={
            "slug": self.kwargs["slug"]
        })
        month_no = int(validateMonth(context["month"])["number"])
        requested_date = datetime.datetime(int(context["year"]), month_no, int(context["date"])).date()
        current_date = datetime.datetime.now().date()
        if requested_date < current_date:
            context["form_not_accepted"] = True
        else:
            context["form_not_accepted"] = False
        return context
    
    # This method called when a valid form is submitted
    def form_valid(self, form):
        context = self.get_context_data()
        try:
            task = self.get_object()
            if task.task == form.cleaned_data["task"]:
                form.errors["custom_error"] = ["Nothing to update."]
                return self.form_invalid(form)   
            task.task = form.cleaned_data["task"]
            task.save()
            context["show_message"] = True # Show message
            context["is_error"] = False # There are no errors
            context["messages"] = self.success_mssg_
            return render(self.request, self.template_name, context)
        except Exception as e:
            # If Unique Constraint fail for duplicate entry on same date
            if "unique_task_date" in str(e):
                form.errors["custom_error"] = ["Task already exist for this date"]
                return self.form_invalid(form)
            else:
                form.errors["custom_error"] = ["Something went wrong, please try again later"]
                return self.form_invalid(form)
        
    # This method is called when a invalid form is submitted
    def form_invalid(self, form):
        context = self.get_context_data()
        context["show_message"] = True # Show message
        context["is_error"] = True # There are errors
        context["messages"] = [error for field_errors in form.errors.values()
                                for error in field_errors] # Flattening Dict of fields(keys): errors (list) 
        return render(self.request, self.template_name, context)


# Class based view for deleting Task
# I am not using DeleteView bcz i am getting confirmation on client side
#  and simply just want to delete and return
class ViewDeleteTask(View):
    def get(self, request, slug):
        try:
            task = Task.objects.get(slug=slug)
            date = task.combine_date.date.data
            month = task.combine_date.month.data
            year = task.combine_date.year.data
            task.delete()
            success_url =  reverse_lazy("tasks:url-date-data", kwargs={"date": date, "year": year, "month": month})
            return HttpResponseRedirect(success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse_lazy("tasks:url-error"))


# Registration class based view
# i can also use FormView here, same as above CreateView implementation
# but for learning purpose i use this
class ViewRegister(View):
    def get(self, request):
        context = dict()
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["form"] = RegisterForm()
        return render(request, "tasks/authenticate/register.html", context)
    
    def post(self, request):
        try:
            context = dict()
            context["app_name"] = settings.PROJECT_APPLICATION_NAME
            context["error"]  = True
            # Basic form validation based on field and its parameters takes place during initialization
            form = RegisterForm(request.POST)
            context["form"]  = form
            email = request.POST.get("email")
            username = request.POST.get("username")
            existing_user_list = get_user_model().objects.filter(Q(username=username) | Q(email=email))
            if len(existing_user_list) > 0 and not existing_user_list[0].is_active:
                # Sending verification mail if account regsitered but not verified
                send_mail_user_verify(existing_user_list[0])
                form.errors["custom"] = ["An inactive account is already registered with given \
username or email, please check your email for instructions to activate it."]
            elif form.is_valid():
                if form.cleaned_data.get("password") != form.cleaned_data.get("confirm_password"):
                    form.errors["custom_error"] = ["Password and confirm password did not match."]
                    raise Exception
                else:
                    # Creating User
                    user = get_user_model().objects.create_user(
                        username=form.cleaned_data.get("username"),
                        email=form.cleaned_data.get("email"),
                        password=form.cleaned_data.get("password"),
                    )
                    
                    # Sending Mail to user for email verification
                    send_mail_user_verify(user)
                    context["error"]  = False
                    form.errors["custom"] = ["Account registered successfully, \
please check your email to activate your account."]
            else:
                raise Exception
        except Exception as e:
            print("Development Error : Creating Account :", e)
            if len(form.errors) <= 0:
                form.errors["custom"] = ["Something went wrong, please try again later."]
        return render(request, "tasks/authenticate/register.html", context)


# Class based login view based on LoginView of django auth system
class ViewLogin(View):
    def get(self, request):
        context = dict()
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["form"] = LoginForm()
        return render(request, "tasks/authenticate/login.html", context)

    def post(self, request):
        try:
            context = dict()
            form  = LoginForm(request.POST)
            context["form"] = form
            context["app_name"] = settings.PROJECT_APPLICATION_NAME

            if form.is_valid():
                # In form class we make sure that if either user provide email or
                # username username_or_email field will only contain user's username
                username = form.cleaned_data.get("username_or_email")
                password = form.cleaned_data.get("password")
                # Authenticate on basis of username and password return user or None
                user = authenticate(request, username=username, password=password)
                if isinstance(user, None.__class__):
                    form.errors["custom"] = ["Invalid credentials for username and password."]
                    raise Exception
                else:
                    login(request, user)
                    return HttpResponseRedirect(reverse("tasks:url-index-default"))
            else:
                raise Exception

        except Exception as e:
            print("Development Error : Login :", e)
            context["error"] = True
            if len(form.errors) <= 0:
                form.errors["custom"] = ["Something went wrong, please try again later."]
            return render(request, "tasks/authenticate/login.html", context)
        

# Class based view for logging out user from sessions and applications
# Using django auth system provided LogoutView because that's enough for us
class ViewLogout(LogoutView):
    next_page = reverse_lazy("tasks:url-login")


# Class based view for passoword change request
class ViewRequestPasswordChange(View):
    def get(self, request):
        context = dict()
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["form"] = PasswordChangeRequestForm()
        return render(request, "tasks/authenticate/forgot_password_request.html", context)

    def post(self, request):
        try:
            context = dict()
            context["error"] = True
            context["app_name"] = settings.PROJECT_APPLICATION_NAME
            form = PasswordChangeRequestForm(request.POST)
            context["form"] = form
            if form.is_valid():
                identifier = form.cleaned_data.get("username_or_email")
                user = get_user_model().objects.get(Q(username=identifier) | Q(email=identifier))

                # Sending verification mail for forgot password
                send_mail_user_verify(user, is_forgot_password=True)
                context["error"] = False
                form.errors["custom"] = \
                    ["Details verified please check your email for further instructions."]
            else:
                raise Exception
        except Exception as e:
            print("Development Error : ViewRequestPasswordChange :", e)
            if len(form.errors) <= 0:
                form.errors["custom"] = ["Something went wrong, please try again later."]
        return render(request, "tasks/authenticate/forgot_password_request.html", context)


# Class based view for passoword change confirmation
class ViewConfirmPasswordChange(View):
    def get(self, request, identifier, uidb64):
        context = dict()
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["error"] = True
        context["disable"] = True
        try:
            form = PasswordChangeConfirmForm()
            context["form"] = form
            user_id, expiry_time = urlsafe_base64_decode_with_expiry(uidb64)
            user = get_user_model().objects.get(pk=int(user_id))
            indentifier_now = generate_user_token(user)
            current_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
            context["username"] = user.username
            context["submit_url"] = reverse("tasks:url-forgot-password-confrim", 
                kwargs={"identifier": identifier, "uidb64": uidb64})
            # ensuring link to this page is not outdated
            if int(current_timestamp) < int(expiry_time):
                # Ensuring right user is accessinng the form
                if indentifier_now == identifier:
                    context["disable"] = False
                else:
                    context["disable_message"] = "Invalid access to this page."
            else:
                context["disable_message"] = "Link expired for this page, please try again."
        except Exception as e:
            print("Development Error : ViewConfirmPasswordChange - Get :", e)
            if len(form.errors) <= 0:
                context["disable_message"] = "Something went wrong, please try again later."
        return render(request, "tasks/authenticate/forgot_password_confirm.html", context)
    
    def post(self, request, identifier, uidb64):
        context = dict()
        context["app_name"] = settings.PROJECT_APPLICATION_NAME
        context["error"] = True
        context["disable"] = False
        try:
            form = PasswordChangeConfirmForm(request.POST)
            context["form"] = form
            user_id, expiry_time = urlsafe_base64_decode_with_expiry(uidb64)
            user = get_user_model().objects.get(pk=int(user_id))
            indentifier_now = generate_user_token(user)
            current_timestamp = datetime.datetime.timestamp(datetime.datetime.now())
            context["username"] = user.username
            context["submit_url"] = reverse("tasks:url-forgot-password-confrim", 
                kwargs={"identifier": identifier, "uidb64": uidb64})
            # ensuring link to this page is not outdated
            if int(current_timestamp) < int(expiry_time):
                # Ensuring right user is accessinng the form
                if indentifier_now == identifier:
                    if form.is_valid():
                        password = form.cleaned_data.get("password")
                        confirm_password = form.cleaned_data.get("confirm_password")
                        if password == confirm_password:
                            user.set_password(password)
                            user.save()
                            context["error"] = False
                            context["disable"] = True
                            context["disable_message"] = "Password change successfully."
                        else:
                            form.errors["custom"] = ["Password and confirm password didn't match."]
                    else:
                        raise Exception
                else:
                    form.errors["custom"] = ["Invalid and unauthorized submission."]
            else:
                form.errors["custom"] = ["Link expired for this submission."]
        except Exception as e:
            print("Development Error : ViewConfirmPasswordChange :", e)
            if len(form.errors) <= 0:
                form.errors["custom"] = ["Something went wrong, please try again later."]
        return render(request, "tasks/authenticate/forgot_password_confirm.html", context)
    

# Handle email verification for registered user
def view_verfiy_email(request, token, uidb64):
    context = dict()
    context["app_name"] = settings.PROJECT_APPLICATION_NAME
    context["fail"] = False
    context["button_message"] =  "Go to Login Page"
    context["button_url"] = reverse("tasks:url-login")
    try:
        user_id, expiry_time = urlsafe_base64_decode_with_expiry(uidb64)
        current_time = int(datetime.datetime.timestamp(datetime.datetime.now()))
        user = get_user_model().objects.get(pk=int(user_id))
        # If current time is greater than token expiry time its invalid
        if current_time < int(expiry_time):
            current_token = generate_user_token(user)
            # If token matches
            if current_token == token:
                # If it is a forgot password verification
                if request.resolver_match.url_name == "url-forgot-password-verify":
                    context["label_message"] = "Successfully verified, click the \
button below for further instructions."
                    context["button_message"] = "Change Password"
                    identifier = generate_user_token(user)
                    uidb64_with_expiry = urlsafe_base64_encode_with_expiry(user)
                    context["button_url"] = reverse("tasks:url-forgot-password-confrim", 
                        kwargs={"identifier": identifier, "uidb64": uidb64_with_expiry})
                # If it is a registration verification
                else:
                    user.is_active = True
                    user.save()
                    context["label_message"] = "Your email has been successfully verified."
            # If token fails
            else:
                raise Exception
        else:
            context["fail"] = True
            context["label_message"] = "Link expired, please check your email for further instructions"
            # Send appropriate email again
            if request.resolver_match.url_name == "url-forgot-password-verify":
                send_mail_user_verify(user, is_forgot_password=True)
            else:
                send_mail_user_verify(user)
    except Exception as e:
        context["fail"] = True
        context["label_message"] = "Email verification failed."
    return render(request, "tasks/authenticate/verification_successful.html", context)