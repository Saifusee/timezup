from django.apps import apps
import datetime

# After Database creation for Tasks seed mandatory data
def postMigrateSignalHandler(sender, **kwargs):

    # Only if app is Tasks
    if type(sender) == type(apps.get_app_config("tasks")):
        month_list = ["january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"]
        ten_years_before = datetime.datetime.now().year - 10

        # Seed Dates from 1 to 31
        Date = apps.get_model("tasks", "Date")
        for i in range(1, 32):
            Date.objects.get_or_create(data=i)

        # Seed Month from January to December
        Month = apps.get_model("tasks", "Month")
        for month in month_list:
            Month.objects.get_or_create(data=month)

        # Seed Year 10 years before and after current year
        Year = apps.get_model("tasks", "Year")
        for year in range(ten_years_before, ten_years_before + 20):
            Year.objects.get_or_create(data=year)

