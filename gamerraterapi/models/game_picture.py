from django.db import models

class Game_Picture(models.Model):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
