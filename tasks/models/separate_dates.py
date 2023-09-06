from django.db import models

# List of Possible Georgarian Dates
class Date(models.Model):
    date_id = models.SmallAutoField(primary_key=True)
    data = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return str(self.data)

# List of Possible Georgarian Months
class Month(models.Model):
    month_id = models.SmallAutoField(primary_key=True)
    data = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return str(self.data.title())

    class Meta:
        ordering = ["month_id"]

# List of Possible Georgarian Years
class Year(models.Model):
    year_id = models.SmallAutoField(primary_key=True)
    data = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return str(self.data)
