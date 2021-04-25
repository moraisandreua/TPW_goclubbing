from django import forms
from app.models import Event_Type, Event


class EditProfileForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100)
    location = forms.CharField(label="Location:", max_length=100)
    type = forms.CharField(label="Type:", max_length=50)
    company_name = forms.CharField(label="Company:", max_length=100)
    opening_hours = forms.JSONField()
    contact_phone = forms.IntegerField(label="Phone Number:")
    contact_email = forms.EmailField(label="Email:")


class AddEventForm(forms.Form):
    name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    datetime = forms.DateTimeField()
    type = forms.ModelChoiceField(queryset=Event_Type.objects.all())
    theme = forms.CharField(max_length=100)
    min_age = forms.IntegerField()
    organization = forms.CharField(max_length=100)
    dress_code = forms.CharField(max_length=100)


class EditEventForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100)
    location = forms.CharField(label="Location:", max_length=100)
    datetime = forms.DateTimeField(label="Date:")
    type = forms.ModelChoiceField(queryset=Event_Type.objects)
    theme = forms.CharField(label="Theme:", max_length=100)
    min_age = forms.IntegerField(label="Minimum age:")
    organization = forms.CharField(label="Organization:", max_length=100)
    dress_code = forms.CharField(label="Dress Code:", max_length=100)


class AddAdvertForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects)
    date = forms.DateTimeField()
    expire = forms.DateTimeField()
    body = forms.CharField(max_length=100)

class EditAdvertForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects)
    date = forms.DateTimeField()
    expire = forms.DateTimeField()
    body = forms.CharField(max_length=100)


class Register(forms.Form):
    name = forms.CharField(label='Business name:', max_length=30)
    location = forms.CharField(label='Business city:', max_length=30)
    type = forms.CharField(label='Business type (ex: Bar):', max_length=15)
    company = forms.CharField(label='Company name:', max_length=30)
    email = forms.EmailField(label='Company email:', max_length=100)
    phone = forms.IntegerField(min_value=900000000, max_value=999999999)
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
