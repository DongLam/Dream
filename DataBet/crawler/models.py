from django.db import models
from django_mongodb_engine.contrib import MongoDBManager
# Create your models here.


class Match(models.Model):
    objects = MongoDBManager()
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    odds1 = models.DecimalField(max_digits=10, decimal_places=5)
    odds2 = models.DecimalField(max_digits=10, decimal_places=5)
    dateTimeStamp = models.DateTimeField(blank=True)
    site = models.CharField(max_length=50, blank=True)
    game = models.CharField(max_length=50, blank=True)
    team1_tmp = models.CharField(max_length=50, blank=True)
    team2_tmp = models.CharField(max_length=50, blank=True)
    league = models.CharField(max_length=100, blank=True)
    datetime = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['team1']