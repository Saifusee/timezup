from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
import re


class PasswordChangeRequestForm(forms.Form):
    username_or_email = forms.CharField(max_length=254, label="Username or E-mail", 
        error_messages={
            "required": "Email Field is mandatory",
            "max_length": "Maximum 254 characters allowed",
            "invalid": "Invalid email input, must follow example@domain.com",
            },
        widget=forms.TextInput(attrs={"placeholder": "Username or Password"})
        )

    def clean_username_or_email(self):
        value = self.cleaned_data.get("username_or_email")

        if re.fullmatch(settings.EMAIL_REGEX, value):
            if not get_user_model().objects.filter(email=value).exists():
                raise forms.ValidationError("No account asssociated with given email address found.", 
                    code="invalid")
        elif re.fullmatch(settings.USERNAME_REGEX, value):
            if not get_user_model().objects.filter(username=value).exists():
                raise forms.ValidationError("No account asssociated with given username found.",
                    code="invalid")
        else:
            raise forms.ValidationError("Invalid email or username format", code="invalid")
        
        return value
