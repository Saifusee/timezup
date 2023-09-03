from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.viewIndex, name='url-index-default'),
    path('select', views.viewSelectYear, name='url-select-year'),
    path('error', views.viewRenderErrorTemplate, name='url-error'),

     ### Authentication - public urls ###
    path('login', views.ViewLogin.as_view(), name='url-login'),
    path('register', views.ViewRegister.as_view(), name='url-register'),
    path('logout', views.ViewLogout.as_view(), name='url-logout'),
    path('register/<str:token>/verify-email/<str:uidb64>', views.view_verfiy_email, 
         name='url-register-email-verify'),
    path('register/<str:token>/verify-forgot-password/<str:uidb64>', views.view_verfiy_email, 
         name='url-forgot-password-verify'),
    path('f_pass/request', views.ViewRequestPasswordChange.as_view(), 
         name='url-forgot-password-request'),
    path('f_pass/<str:identifier>/<str:uidb64>/confirm', views.ViewConfirmPasswordChange.as_view(), 
         name='url-forgot-password-confrim'),
     #####################################

    path('<int:year>', views.viewIndex, name='url-index-year'),
    path('<slug:slug>/edit', views.ViewEditTask.as_view(), name='url-edit-task'),
    path('<slug:slug>/delete', views.ViewDeleteTask.as_view(), name='url-delete-task'),
    path('<int:year>/<str:month>', views.viewShowMonthDates, name='url-month-data'),
    path('<int:year>/<str:month>/<int:date>/data', views.viewShowDateData, name='url-date-data'),
    path('<int:year>/<str:month>/<int:date>/create', views.ViewCreateTask.as_view(), name='url-create-task'),
]



# List of public page urls which unauthenticated user can access
# Custom list, not django specific
PUBLIC_URLS = [
    "url-login",
    "url-register",
    "url-register-email-verify",
    "url-forgot-password-verify",
    "url-forgot-password-request",
    "url-forgot-password-confrim",
    "url-error",
]
