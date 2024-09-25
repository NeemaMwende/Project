from django import forms
from django.contrib.auth.forms import UserCreationForm  # Correct capitalization

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": "True", "class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = UserCreationForm.Meta.model  # Use the same model as UserCreationForm
        fields = ('username', 'email', 'password1', 'password2')  # Specify the fields you want in your form
