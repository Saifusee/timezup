from django.db import models
from tasks.models.separate_dates import Date, Month, Year

class CombineDate(models.Model):
    date = models.ForeignKey(Date, on_delete=models.PROTECT, null=False)
    month = models.ForeignKey(Month, on_delete=models.PROTECT, null=False)
    year = models.ForeignKey(Year, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return f"{self.month.data.title()} {self.date.data}, {self.year.data}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["date", "month", "year"], 
                name="unique_dates", 
                violation_error_message="Combination of Date already exist")
        ]
        verbose_name = "Date of the Task"