from django import forms 
from .models import CustomUser, Client, Worker

# User registration form
class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=150, required=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

# Client registration form
class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['company_name','state', 'LGA', 'phone_number']

# Worker registration form
class WorkerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['state', 'LGA', 'phone_number', 'specialization',]
