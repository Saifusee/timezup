from django.shortcuts import render
from django.http import Http404
import datetime
from timezup.settings import PROJECT_APPLICATION_NAME
from .models import CombineDate, Task, Year, Month, Date
from django.db.models import Q


# Validate aceepted year value
def validateYear(year):
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
    try:
        end_date = get_month_end_date(month, year)
        # either given value map to id or data
        rec_date = Date.objects.get(Q(data=date) & Q(data__lte=end_date))
        return rec_date.data
    except Exception:
        raise Http404("Development: Invalid Date")
    

def get_month_end_date(month : int, year: int) -> int:
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


# Index first page , months rendering
def index(request, year=None):
    year = validateYear(year)
    months_data = Month.objects.all()

    context = {
        'year': year,
        'months_data': months_data,
        'app_name': PROJECT_APPLICATION_NAME
    }
    return render(request, 'tasks/index.html', context)


# Select year
def selectYear(request):
    current_year = int(datetime.datetime.now().strftime('%Y'))
    context = {
        'current_year': current_year,
        'app_name': PROJECT_APPLICATION_NAME
    }
    return render(request, 'tasks/years.html', context)


# Month wise dates rendering
def showMonthDates(request, year, month):
    
    year = validateYear(year)
    month = validateMonth(month)
    end = get_month_end_date(month["number"], year)

    context = {
        'app_name': PROJECT_APPLICATION_NAME,
        'year': year,
        'month_name': month["name"],
        'end_date': end
    }
    return render(request, 'tasks/month_dates.html', context)


# Date wise data show
def showDateData(request, year, month, date):
    year = validateYear(year)
    month = validateMonth(month)
    date = validateDate(date, month['number'], year)
    
    year_inst = Year.objects.get(data=year)
    month_inst = Month.objects.get(pk=month["number"])
    date_inst = Date.objects.get(data=date)

    # since get_or_create return (object, created)
    combine_date, _ = CombineDate.objects.get_or_create(year=year_inst, month=month_inst, date=date_inst)
    tasks = Task.objects.filter(combine_date=combine_date)
    context = {
        'app_name': PROJECT_APPLICATION_NAME,
        'year': year,
        'month': month["name"],
        'date': date,
        'tasks': tasks,
    }

    return render(request, 'tasks/dates.html', context)


# Create New Task
def createEditTask(request, year=None, month=None, date=None, task_id=None):
    title = 'Create New'
    if not type(task_id) == None.__class__:
        title = ' Edit'
        year = 'Default'
        month = 'Default'
        date = 'Default'
        year = 'Default'
    context = {
        'app_name': PROJECT_APPLICATION_NAME,
        'year': year,
        'month': month,
        'date': date,
        'title': title,
        'message': 'Created Successfulyy horah horah vah avatar'
    }
    return render(request, 'tasks/form.html', context)


# Delete New Task
def deleteTask(request, task_id):
    pass
