from django.db import models
from tasks.models.combine_date import CombineDate
from datetime import datetime
import hashlib
from django.utils.text import slugify
from django.contrib.auth import get_user_model


class Task(models.Model):
    task = models.TextField(max_length=500)
    combine_date = models.ForeignKey(CombineDate, on_delete=models.PROTECT, null=False)
    slug = models.SlugField(max_length=50, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, 
        related_name="task_set", related_query_name="tasks")
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    # Overriding save to insert additinal functionality
    def save(self, *args, **kwargs):
        if isinstance(self.slug, None.__class__):
            task = self.task if len(self.task) < 50 else self.task[:15]
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = date + task
            hashed_data = hashlib.md5(data.encode("utf-8")).hexdigest()
            self.slug = slugify(hashed_data) if len(hashed_data) < 50 else slugify(hashed_data[:50])
        super().save(*args, **kwargs)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["task", "combine_date"],
                name="unique_task_date",
                violation_error_message="Task already exist for this date"),
            models.UniqueConstraint(fields=["slug"], 
                name="unique_hash_id", violation_error_message="Hash identifier already exists")
        ]