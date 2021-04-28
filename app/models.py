from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=100, default="")
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    opening_hours = models.JSONField(null=True)
    contact_email = models.EmailField(max_length=100)
    contact_phone = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePhoto = models.FileField(upload_to="business_photos/", default="business_photos/userDefault.png")

    def __str__(self):
        return self.name


class BusinessPhoto(models.Model):
    path = models.FileField(upload_to="business_photos/")
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

class Event_Type(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    type = models.ForeignKey(Event_Type, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100)
    min_age = models.IntegerField()
    organization = models.CharField(max_length=100)
    dress_code = models.CharField(max_length=100)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EventPhoto(models.Model):
    path = models.FileField(upload_to="event_photos/")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Comment(models.Model):
    classification = models.IntegerField()
    body = models.CharField(max_length=1024)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class Advertisement(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date=models.DateTimeField()
    expire=models.DateTimeField()
    body=models.CharField(max_length=100)

"""

{
    "days":[
        {
            "day":"Thursday",
            "hours":{
                "opening": #HORA#,
                "closing": #HORA#
            }
        },
        {
            "day":"Friday",
            "hours":{
                "opening": #HORA#,
                "closing": #HORA#
            }
        },
        {
            "day":"Saturday",
            "hours":{
                "opening": #HORA#,
                "closing": #HORA#
            }
        }
    ]
}
"""
