from django.db import models
from django.contrib.auth.models import User
from .review import Review

class Game(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    year = models.IntegerField()
    players = models.IntegerField()
    age = models.IntegerField()
    time = models.IntegerField()

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        reviews = Review.objects.filter(game=self)
        # Sum all of the ratings for the game
        total_rating = 0
        rating = 0
        for review in reviews:
            total_rating += review.rating
        if len(reviews)>0:
            rating = total_rating /len(reviews)
        return rating
        # If you don't know how to calculate averge, Google it.
