from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('worker', 'Worker'),
    )
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)
    company_name = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=True)
    lga = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'first_name', 'last_name', 'company_name', 'state', 'lga', 'phone_number')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        if user_type == 'client':
            if not cleaned_data.get("company_name"):
                self.add_error('company_name', "Company name is required for clients.")
        elif user_type == 'worker':
            if not cleaned_data.get("first_name"):
                self.add_error('first_name', "First name is required for workers.")
            if not cleaned_data.get("last_name"):
                self.add_error('last_name', "Last name is required for workers.")

        return cleaned_data
