from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    ISBN_MAX_LENGTH = 13

    isbn = models.CharField(max_length=ISBN_MAX_LENGTH, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_year = models.CharField(max_length=4, null=True)
    country = models.CharField(max_length=255, default = "N/A")
    cover = models.ImageField(upload_to='cover_images', blank=True, null = True)
    description = models.TextField(max_length=1000, blank=True, null = True)

    def __str__(self):
        return self.isbn
    

class Puzzle(models.Model):
    puzzleID = models.IntegerField(unique=True, primary_key=True)

    date = models.DateField(unique=True)
    isbn = models.OneToOneField(Book, on_delete=models.CASCADE)
    difficulty = models.FloatField(default=0.0)
    popularity = models.FloatField(default=0.0)

    def __str__(self):
        return self.date


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.IntegerField(unique=True, primary_key=True)
    
    # Faraj to complete

    def __str__(self):
        return self.user.username
        

class Score(models.Model):
    scoreID = models.IntegerField(unique=True, primary_key=True)

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    guesses = models.IntegerField(default=10)
    difficulty = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    puzzleID = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    def __str__(self):
        return self.guesses
    
class Comment(models.Model):
    commentID = models.IntegerField(unique=True, primary_key=True)

    puzzleID = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

