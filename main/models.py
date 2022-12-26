from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Anime(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    synopsis = models.TextField()
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    rank = models.IntegerField(validators=[MinValueValidator(1)])
    popularity = models.IntegerField(validators=[MinValueValidator(1)])
    episodes = models.IntegerField(validators=[MinValueValidator(0)])
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    studios = models.ManyToManyField('Studio')
    genres = models.ManyToManyField('Genre')


class Type(models.Model):
    name = models.CharField(max_length=50)


class Status(models.Model):
    name = models.CharField(max_length=50)


class Studio(models.Model):
    name = models.CharField(max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=50)
