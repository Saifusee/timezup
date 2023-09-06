from django import forms
from tasks.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task"]
        labels = {
            "task": "Enter Task"
        }
        widgets = {
            "task": forms.Textarea(
                attrs={
                    "class": "txtinpt",
                    "id": "task",
                    "cols": 30,
                    "rows": 10
                    }
                )
        }
        error_messages = {
            "task": {
                "required": "Task Field is mandatory",
                "max_length": "Maximum 255 characters allowed"
            }
        }
