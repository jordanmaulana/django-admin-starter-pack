# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

from apps.profiles.models import Profile

# admin.py


# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on"]
