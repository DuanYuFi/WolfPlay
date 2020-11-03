from django.contrib import admin

# Register your models here.
from .models import User, Room, Game

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Game)