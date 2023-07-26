from django.shortcuts import render
from django.http import HttpResponse, Http404
import datetime
from timezup.settings import APP_NAME


database = {
    "january": [
        "Complete online Python course",
        "Read 2 books on programming"
    ],
    "february": [
        "Read 3 books on personal development",
        "Practice yoga 3 times a week"
    ],
    "march": [
        "Exercise at least 4 times a week",
        "Learn to play a new board game"
    ],
    "april": [
        "Start a daily meditation practice",
        "Explore hiking trails on weekends"
    ],
    "may": [
        "Learn to cook 5 new recipes",
        "Attend a photography workshop"
    ],
    "june": [
        "Save 20% of monthly income",
        "Write a short story"
    ],
    "july": [
        "Take a weekend trip to a new city",
        "Learn to swim"
    ],
    "august": [
        "Learn a new musical instrument",
        "Practice mindfulness meditation"
    ],
    "september": [
        "Enroll in a foreign language course",
        "Volunteer at a local shelter"
    ],
    "october": [
        "Volunteer for a charitable organization",
        "Start a fitness challenge with friends"
    ],
    "november": [
        "Set up a personal website/portfolio",
        "Read a classic novel"
    ],
    "december": [
        "Plan and execute a holiday party",
        "Create a vision board for the next year"
    ]
}


# Index first page , months rendering
def index(request, year=None):
    if isinstance(year, None.__class__):
        year = int(datetime.datetime.now().strftime('%Y'))

    context = {
        'year': year,
        'months_data': database,
        'app_name': APP_NAME
    }
    return render(request, 'tasks/index.html', context)


# Select year
def selectYear(request):
    current_year = int(datetime.datetime.now().strftime('%Y'))
    context = {
        'current_year': current_year,
        'app_name': APP_NAME
    }
    return render(request, 'tasks/years.html', context)


# Month wise dates rendering
def showMonthDates(request, year, month_no=None, month_name=None):
    if month_name is None and month_no is None:
        raise Http404("Development: Page not Found")
    elif month_name is not None:
        month_index = list(database.keys()).index(month_name)
        return showMonthDates(request, year, month_no=(month_index + 1))
    else:
        if month_no < 1 or month_no > 12:
            raise Http404('Development: Invalid Month')
        elif month_no % 2 == 0 and month_no == 2:
            if year % 4 == 0:
                end = 30
            else:
                end = 29
        elif month_no % 2 == 0 and month_no <= 7:
            end = 31
        elif month_no % 2 == 0 and (month_no > 7 and month_no <= 12):
            end = 32
        elif month_no % 2 != 0 and (month_no > 7 and month_no <= 12):
            end = 31
        else:
            end = 32

        context = {
            'app_name': APP_NAME,
            'year': year,
            'month_name': list(database.keys())[month_no-1],
            'end_date': end
        }
        return render(request, 'tasks/month_dates.html', context)


# Date wise data show
def showDateData(request, year, month, date):
    ### Remeber to put validators for date month no and name while db is ready ############
    ### Remeber to put validators for date month no and name while db is ready ############
    ### Remeber to put validators for date month no and name while db is ready ############
    ### Remeber to put validators for date month no and name while db is ready ############
    ### Remeber to put validators for date month no and name while db is ready ###############

    if month.isdigit():
        month = list(database.keys())[month-1]
    
    context = {
        'app_name': APP_NAME,
        'year': year,
        'month': month,
        'date': date,
        'data': 'This is my dummy task and i This is my dummy task and iThis is my dummy task and i This is my dummy task and i This is my dummy task and iThis is my dummy task and i This is my dummy task and i This is my dummy task and iThis is my dummy task and i This is my dummy task and i This is my dummy task and i This is my dummy task and iThis is my dummy task and i This is my dummy task and i This is my dummy task and iThis is my dummy task and i This is my dummy task and i This is my dummy task and iTa',
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
        'app_name': APP_NAME,
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