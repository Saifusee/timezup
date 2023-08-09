from django.db import models
from tasks.models.combine_date import CombineDate


class Task(models.Model):
    task = models.TextField(max_length=500)
    combine_date = models.ForeignKey(CombineDate, on_delete=models.PROTECT, null=False)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["combine_date"])
        ]
        constraints = [
            models.UniqueConstraint(fields=["task", "combine_date"],
                name="unique_task_date",
                violation_error_message="Task already exist for this date")
        ]
