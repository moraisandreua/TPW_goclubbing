from django import forms

class Register(forms.Form):
    name = forms.CharField(label='Business name:', max_length=30)
    location = forms.CharField(label='Business city:', max_length=30)
    type = forms.CharField(label='Business type (ex: Bar):', max_length=15)
    company = forms.CharField(label='Company name:', max_length=30)
    email = forms.EmailField(label='Company email:', max_length=100)
    phone = forms.IntegerField(min_value=900000000, max_value=999999999)
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
