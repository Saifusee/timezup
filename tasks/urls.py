from django.urls import path
from tasks import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='url-index-default'),
    path('select', views.selectYear, name='url-select-year'),
    path('<int:year>', views.index, name='url-index-year'),
    path('<str:task_id>/edit', views.createEditTask, name='url-edit-task'),
    path('<str:task_id>/delete', views.deleteTask, name='url-delete-task'),
    path('<int:year>/<str:month>', views.showMonthDates, name='url-month-data'),
    path('<int:year>/<str:month>/<int:date>/data', views.showDateData, name='url-date-data'),
    path('<int:year>/<str:month>/<int:date>/create', views.createEditTask, name='url-create-task'),
]
