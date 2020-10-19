from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length = 50)
    password = models.CharField(max_length = 100)
    e_mail = models.EmailField()
    isLogin = models.BooleanField(default = False)
    friends = models.TextField(default = '[]')