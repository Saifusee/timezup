from django import forms
import re
from django.contrib.auth import get_user_model
from django.conf import settings


# Validate Password against regex
def validate_password(object, field_name):
    value = object.cleaned_data[field_name]
    regex = settings.PASSWORD_REGEX
    field_title = "Confirm Password" if field_name == "confirm_password" else "Password"
    error_message = f"{field_title} must be between 8 to 124 character, \
        and must contain atleast one number, special symbol, capital and small letter"
    if not re.fullmatch(regex, value):
        raise forms.ValidationError(error_message, code="invalid")
    # All methods prefix with clean must return their fields cleaned value or raise ValidationError
    return value


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=128,
        widget=forms.TextInput(attrs={"placeholder": "Confirm Password", "autocomplete": "off"}))

    # Validate Username
    def clean_username(self):
        # Since clean() is called already so cleaned_data is set
        value = self.cleaned_data["username"]
        regex = settings.USERNAME_REGEX
        if not re.fullmatch(regex, value):
            error_message = "Username must contain alphanumeric characters, underscore and period onlys"
            raise forms.ValidationError(error_message, code="invalid")
        
        # Must return field value which is cleaned_data
        return value

    # Validate Password
    def clean_password(self):
        return validate_password(self, "password")

    # Validate Confirm Password
    def clean_confirm_password(self):
        return validate_password(self, "confirm_password")

    # This doesn't call automatically, its a helper method
    def validate_password(self, field_name):
        value = self.cleaned_data[field_name]
        regex = settings.PASSWORD_REGEX
        field_title = "Confirm Password" if field_name == "confirm_password" else "Password"
        error_message = f"{field_title} must be between 8 to 124 character, \
            and must contain atleast one number, special symbol, capital and small letter"
        if not re.fullmatch(regex, value):
            raise forms.ValidationError(error_message, code="invalid")
        # All methods prefix with clean must return their fields cleaned value or raise ValidationError
        return value
    
    # Email validation not needed because it automatically taken care

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "confirm_password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Password", "show": "*"})
        }
        error_messages = {
            "username": {
                "required": "Username Field is mandatory",
                "max_length": "Maximum 50 characters allowed",
                "unique": "Username already linked to another account"
            },
            "email": {
                "required": "Email Field is mandatory",
                "max_length": "Maximum 254 characters allowed",
                "invalid": "Invalid email input, must follow example@domain.com",
                "unique": "E-mail already linked to another account"
            },
            "password": {
                "required": "Password Field is mandatory",
                "max_length": "Maximum 128 characters allowed"
            },
            "confirm_password": {
                "required": "Confirm Password Field is mandatory",
                "max_length": "Maximum 128 characters allowed"
            }
        }