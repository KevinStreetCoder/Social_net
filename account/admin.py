from django.contrib import admin
from .models import profile

@admin.register(profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birth','photo']
