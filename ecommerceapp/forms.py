from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm # Correct capitalization

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": "True", "class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class":"form-control"}))
    
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": "True", "class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        #model = User
        model = UserCreationForm.Meta.model  # Use the same model as UserCreationForm
        fields = ('username', 'email', 'password1', 'password2')  # Specify the fields you want in your form

class MyPasswordResetForm(PasswordChangeForm):
    pass
    
class CustomerProfileForm(forms.ModelForm):
    