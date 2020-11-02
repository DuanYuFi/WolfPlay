from django.contrib import admin

# Register your models here.
from .models import User, Room

admin.site.register(User)
admin.site.register(Room)