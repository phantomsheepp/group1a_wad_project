from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    ISBN_MAX_LENGTH = 13

    isbn = models.CharField(max_length=ISBN_MAX_LENGTH, unique=True, default='Unknown')
    title = models.CharField(max_length=100, default='Unknown')
    author = models.CharField(max_length=100, default='Unknown')
    genre = models.CharField(max_length=50, default='Unknown')
    release_year = models.CharField(max_length=4, default='0000')
    country = models.CharField(max_length=255, default='Unknown')
    cover = models.ImageField(upload_to='cover_images', blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.isbn
    

class Puzzle(models.Model):
    puzzleID = models.IntegerField(unique=True, primary_key=True, default=0)

    date = models.DateField(unique=True, default='2000-01-01')
    isbn = models.OneToOneField(Book, on_delete=models.CASCADE, default=None)
    difficulty = models.FloatField(default=0.0)
    popularity = models.FloatField(default=0.0)

    def __str__(self):
        return self.date


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    user_picture = models.ImageField(upload_to='profile_images', blank=True, default=None)
    bio = models.CharField(blank=True, default="Write a bio! ", max_length=250)
    slug = models.SlugField(blank=True, default='')  # Add this line

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        

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

