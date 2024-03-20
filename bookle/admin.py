from django.contrib import admin
from bookle.models import UserProfile, Book, Puzzle, Score, Comment

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'release_year')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('puzzleID', 'date', 'difficulty', 'popularity')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('userID', 'guesses', 'puzzleID')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentID', 'userID', 'puzzleID', 'comment')

admin.site.register(Book, BookAdmin)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Comment, CommentAdmin)