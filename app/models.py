from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    opening_hours = models.JSONField(null=True)
    contact_email = models.EmailField(max_length=100)
    contact_phone = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BusinessPhoto(models.Model):
    path = models.FileField()
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    type = models.CharField(max_length=100)
    theme = models.CharField(max_length=100)
    min_age = models.IntegerField()
    organization = models.CharField(max_length=100)
    dress_code = models.CharField(max_length=100)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EventPhoto(models.Model):
    path = models.FileField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Comment(models.Model):
    classification = models.IntegerField()
    body = models.CharField(max_length=1024)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.body.strip(".")[0]  # First sentence is returned

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
