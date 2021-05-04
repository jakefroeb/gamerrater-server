from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    year = models.IntegerField()
    players = models.IntegerField()
    age = models.IntegerField()
    time = models.IntegerField()
