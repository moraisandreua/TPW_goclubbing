from django import forms
from app.models import Event_Type, Event, Business


class EditProfileForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100)
    location = forms.CharField(label="Location:", max_length=100)
    address = forms.CharField(label="Address:", max_length=100)
    type = forms.CharField(label="Type:", max_length=50)
    company_name = forms.CharField(label="Company:", max_length=100)
    opening_hours = forms.JSONField()
    contact_phone = forms.IntegerField(label="Phone Number:")
    contact_email = forms.EmailField(label="Email:")
    profilePhoto = forms.ImageField(label="Profile Image:", required=False, widget=forms.FileInput)
    image = forms.ImageField(label="Add New Business Image:", required=False, widget=forms.FileInput)


class EventForm(forms.Form):
    name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    type = forms.ModelChoiceField(queryset=Event_Type.objects.all())
    theme = forms.CharField(max_length=100)
    min_age = forms.IntegerField()
    organization = forms.CharField(max_length=100)
    dress_code = forms.CharField(max_length=100)
    image = forms.ImageField(label="Add New Event Image:", required=False, widget=forms.FileInput)


class AdvertForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all())
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date-local'}))
    expire = forms.DateTimeField()
    body = forms.CharField(max_length=100)


class Register(forms.Form):
    name = forms.CharField(label='Business name:', max_length=30)
    location = forms.CharField(label='Business city:', max_length=30)
    type = forms.CharField(label='Business type (ex: Bar):', max_length=15)
    company = forms.CharField(label='Company name:', max_length=30)
    email = forms.EmailField(label='Company email:', max_length=100)
    phone = forms.IntegerField(label='Phone Number:', min_value=900000000, max_value=999999999)
    username = forms.CharField(label='Username:', max_length=15)
    password = forms.CharField(label='Password:', max_length=30, widget=forms.PasswordInput())

class Login(forms.Form):
    username = forms.CharField(label='Username:', max_length=15)
    password = forms.CharField(label='Password:', max_length=30, widget=forms.PasswordInput())


class Filter(forms.Form):
    types = []
    type = []
    i = 1
    for x in Business.objects.all():
        if x.type.lower()[0].upper() + x.type.lower()[1:] not in type:
            types.append((x.type.lower()[0].upper() + x.type.lower()[1:], x.type.lower()[0].upper() + x.type.lower()[1:]))
            type.append(x.type.lower()[0].upper() + x.type.lower()[1:])
            i = i+1

    date = forms.DateField(label='Date', widget=forms.SelectDateWidget, required=False)
    location = forms.CharField(label='Location', max_length=30, required=False)
    type = forms.ModelChoiceField(label='Type', queryset=Event_Type.objects, required=False)
    theme = forms.CharField(label='Theme', required=False)
    business = forms.CharField(label='Business', max_length=30, required=False)
    age = forms.IntegerField(required=False)
    name = forms.CharField(label='Event Name', max_length=50, required=False)
    business_type = forms.ChoiceField(choices=tuple(types), widget=forms.Select(), required=False)


