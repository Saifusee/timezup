from django import forms
from django.conf import settings
import re
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": "Username or E-mail"}),
        error_messages={
            "required": "Username or Email field cannot be empty.",
            "max_length": "Maximum of 254 characters allowed in username or email field."
        })
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "show": "*"}),
        error_messages={
            "required": "Password field cannot be empty.",
            "max_length": "Maximum of 128 characters allowed in password field."
        })
    
    def clean_username_or_email(self):
        value = self.cleaned_data.get("username_or_email")
        if re.fullmatch(settings.USERNAME_REGEX, value):
            username = value
        elif re.fullmatch(settings.EMAIL_REGEX, value):
            try:
                user = get_user_model().objects.get(email=value)
                username = user.username
            except Exception:
                raise forms.ValidationError("No account linked to given email address.", code="invalid")
        else:
            raise forms.ValidationError("Given username or email is in invalid format.", code="invalid")
        return username