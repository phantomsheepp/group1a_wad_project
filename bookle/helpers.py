from django.http import HttpResponse
from bookle.models import Book


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