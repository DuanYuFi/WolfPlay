from django.db import models
import uuid
import django.utils.timezone as timezone
import datetime

oneDay = datetime.timedelta(1, 0, 0, 0, 0)
# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 50)
    password = models.CharField(max_length = 100)
    e_mail = models.EmailField()
    isLogin = models.BooleanField(default = False)
    friends = models.TextField(default = '[]')
    isPlaying = models.BooleanField(default = False)
    roomNumber = models.UUIDField(default = uuid.UUID('00000000-0000-0000-0000-000000000000'))
    lastLogin = models.DateTimeField(default = timezone.now)

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    name = models.CharField(max_length= 50, default=None)
    password = models.CharField(max_length=50, default="")
    host = models.UUIDField(default = uuid.UUID('00000000-0000-0000-0000-000000000000'))
    members = models.TextField(default = '[]')
    chats = models.TextField(default = '[]')