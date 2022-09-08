from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=200)
    name_unified = models.CharField(max_length=200)
    url = models.CharField(max_length=200, unique=True)


class Movie(models.Model):
    name = models.CharField(max_length=200)
    name_unified = models.CharField(max_length=200)
    actors = models.ManyToManyField(Actor, related_name='movies')
    url = models.CharField(max_length=200, unique=True)
