from bookle.models import Book, Puzzle, Score
from datetime import datetime


def get_book_names(max_results=0, starts_with=''):
    """
    Finds a specified number of book titles that start with the given string.
    """
    names = []
    if starts_with:
        names = Book.objects.filter(title__istartswith=starts_with) | Book.objects.filter(title__istartswith="the "+starts_with)
    
    if max_results > 0:
        if len(names) > max_results:
            names = names[:max_results]
    
    return names

def get_guess_data(guess, date):
    """
    Retrieves guessed book's data and compares it to the target book's data. By comparing the data,
    it checks whether the attributes should be displayed as a correct guess or close guess. This 
    information is returned as the appropriate CSS class to be used to display the attribute.

    :param guess: user guess as string
    :param date: date of the puzzle being checked against
    :returns: dictionary containing the guessed book's data and the CSS class for each attribute 
    """
    puzzle = Puzzle.objects.filter(date=datetime.strptime(date, '%Y-%m-%d').date())[0]
    target_book = puzzle.isbn

    feedback = {}
    guessed_book = Book.objects.filter(title__iexact=guess)[0]

    feedback["title"] = guessed_book.title
    feedback["author"] = guessed_book.author 
    feedback["release_year"] = str(guessed_book.release_year)
    feedback["no_of_words"] = str(len(guessed_book.title.split(" ")))
    feedback["cover"] = guessed_book.cover


    feedback["author_class"] = "correctGuess" if (guessed_book.author == target_book.author) else ""

    release_year_diff = guessed_book.release_year - target_book.release_year
    if release_year_diff == 0:
        feedback["release_year_class"] = "correctGuess"

    elif abs(release_year_diff) < 10:
        feedback["release_year_class"] = "closeGuess"
        if release_year_diff > 0:
            feedback["release_year"] += " ↓"
        else:
            feedback["release_year"] += " ↑"

    no_of_words_diff = len(guessed_book.title.split(" ")) - len(target_book.title.split(" "))
    if no_of_words_diff == 0:
        feedback["no_of_words_class"] = "correctGuess"

    elif abs(no_of_words_diff) < 3:
        feedback["no_of_words_class"] = "closeGuess"
        if no_of_words_diff > 0:
            feedback["no_of_words"] += " ↓"
        else:
            feedback["no_of_words"] += " ↑"

    return feedback

def check_guess(guess, date):
    """
    Checks whether the string inputted by the user corresponds to an existing book in the database,
    or whether it is the title of the chosen puzzle's book. 

    :param guess: user guess as string
    :param date: date of the puzzle being checked against
    :returns: (boolean, boolean) corresponding to (correct guess, valid guess)
    """
    puzzle = Puzzle.objects.filter(date=datetime.strptime(date, '%Y-%m-%d').date())[0]
    target_book = puzzle.isbn
    
    if not Book.objects.filter(title__iexact=guess):
        return False, False
    elif Book.objects.filter(title__iexact=guess)[0] == target_book:    
        return True, True
    else:
        return False, True
   
def get_target_book_data(puzzle):
    target_book = puzzle.isbn

    data = {}

    data["title"] = target_book.title
    data["author"] = target_book.author 
    data["release_year"] = str(target_book.release_year)
    data["cover"] = target_book.cover

    return data


def check_if_complete(user, puzzle):
    if Score.objects.filter(userID=user, puzzleID=puzzle).exists():
        return 