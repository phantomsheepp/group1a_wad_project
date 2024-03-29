from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    ISBN_MAX_LENGTH = 13

    isbn = models.CharField(max_length=ISBN_MAX_LENGTH, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_year = models.IntegerField(null=True)
    country = models.CharField(max_length=255)
    cover = models.CharField(max_length=300, default='')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.isbn
    

class Puzzle(models.Model):
    puzzleID = models.IntegerField(unique=True, primary_key=True)

    date = models.DateField(unique=True)
    isbn = models.OneToOneField(Book, on_delete=models.CASCADE)
    difficulty = models.FloatField(null=True)
    popularity = models.FloatField(null=True)

    def __str__(self):
        return str(self.date)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_picture = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    bio = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
        

class Score(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    guesses = models.IntegerField(null=True)
    success = models.BooleanField(default=False)
    difficulty = models.IntegerField(choices=RATING_CHOICES, null=True)
    popularity = models.IntegerField(choices=RATING_CHOICES, null=True)
    puzzleID = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.guesses)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userID', 'puzzleID'], name='unique_score')
        ]
    

class Comment(models.Model):
    commentID = models.AutoField(unique=True, primary_key=True)
    puzzleID = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    