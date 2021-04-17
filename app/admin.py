from django.contrib import admin
from app.models import Business, BusinessPhoto, EventPhoto, Event, Comment

# Register your models here.
admin.site.register(Business)
admin.site.register(BusinessPhoto)
admin.site.register(EventPhoto)
admin.site.register(Event)
admin.site.register(Comment)
