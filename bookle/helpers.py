from django.http import HttpResponse
from bookle.models import Book, Puzzle
from datetime import datetime


def get_book_names(max_results=0, starts_with=''):
    """Finds a specified number of book titles that start with the given
    string."""
    names = []
    if starts_with:
        names = Book.objects.filter(title__istartswith=starts_with) | Book.objects.filter(title__istartswith="the "+starts_with)
    
    if max_results > 0:
        if len(names) > max_results:
            names = names[:max_results]
    
    return names

def get_guess_data(guess, date):
    feedback = {}
    guessed_book = Book.objects.filter(title__iexact=guess)[0]

    feedback["title"] = guessed_book.title
    feedback["author"] = guessed_book.author 
    feedback["release_year"] = guessed_book.release_year 
    feedback["no_of_words"] = len(guessed_book.title.split(" ")) 

    return feedback

def check_guess(guess, date):
    puzzle = Puzzle.objects.filter(date=datetime.strptime(date, '%Y-%m-%d').date())[0]
    target_book = puzzle.isbn
    
    if not Book.objects.filter(title__iexact=guess):
        return False, False, {}
    elif Book.objects.filter(title__iexact=guess)[0] == target_book:    
        return True, True, {}
    else:
        feedback = {}
        guessed_book = Book.objects.filter(title__iexact=guess)[0]

        feedback["author"] = 2 if guessed_book.author == target_book.author else 0

        release_year_diff = guessed_book.release_year - target_book.release_year
        if release_year_diff == 0:
            feedback["release_year"] = (2,"")

        elif abs(release_year_diff) < 10:
            if release_year_diff > 0:
                feedback["release_year"] = (1,"down")
            else:
                feedback["release_year"] = (1,"up")
                
        else:
            feedback["release_year"] = (0,"")

        no_of_words_diff = len(guessed_book.title.split(" ")) - len(target_book.title.split(" "))
        if no_of_words_diff:
            feedback["no_of_words"] = 2

        elif abs(no_of_words_diff) < 3:
            if no_of_words_diff > 0:
                feedback["release_year"] = (1,"down")
            else:
                feedback["release_year"] = (1,"up")

        else:
            feedback["no_of_words"] = 0
        
        return False, True, feedback
   