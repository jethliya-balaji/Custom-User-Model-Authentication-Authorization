from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "username",
                  "phone_number", "address", "password1", "password2")

    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()
    
    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_username(self):
        return self.cleaned_data['username'].lower()


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                try:
                    user = Account.objects.get(email=email)
                    if not user.is_active:
                        raise forms.ValidationError("The account You tried to Sign in with is not an active account.")
                except Account.DoesNotExist:
                    raise forms.ValidationError({'email': ["No such email is registered."]})
                raise forms.ValidationError({'password': ["Incorrect password."]})
