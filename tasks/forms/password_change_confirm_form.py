from django import forms
from django.contrib.auth import get_user_model
from tasks.forms.register_form import validate_password

class PasswordChangeConfirmForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128,
        widget=forms.TextInput(attrs={"placeholder": "Confirm Password", "autocomplete": "off"})
        )

    # Validate Password
    def clean_password(self):
        return validate_password(self, "password")

    # Validate Confirm Password
    def clean_confirm_password(self):
        return validate_password(self, "confirm_password")
    
    class Meta:
        model = get_user_model()
        fields = ["password", "confirm_password"]
        error_messages = {
            "password": {
                "required": "Password Field is mandatory",
                "max_length": "Maximum 128 characters allowed"
            },
            "confirm_password": {
                "required": "Confirm Password Field is mandatory",
                "max_length": "Maximum 128 characters allowed"
            }
        }
        widgets ={
            "password": forms.PasswordInput(attrs={"placeholder": "Password"})
        }