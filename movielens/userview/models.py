from django.db import models
from django.contrib.auth.models import AbstractUser

# User
class User(AbstractUser):
    friends = models.ManyToManyField("self")


# FriendRequest
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")


class Image(models.Model):
    url = models.CharField(max_length=1000)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    sortNumber = models.IntegerField()


# Genre
class Genre(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


# Movie
class Movie(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


# Rating
class Rating(models.Model):
    value = models.IntegerField()
    comment = models.CharField(max_length=1000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
