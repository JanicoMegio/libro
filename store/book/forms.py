from django import forms
from django.contrib.auth.models import User
from .models import UserDetails


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['fname', 'lname', 'midname', 'age', 'birthdate', 'contact', 'address1', 'address2']




class SortForm(forms.Form):
    SORT_CHOICES = [
        ('price', 'Price: Low to Highest')
    ]

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)