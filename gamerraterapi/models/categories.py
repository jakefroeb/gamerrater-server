from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, default="")
    game = models.ManyToManyField("Game")
