from django.http import HttpResponse
from bookle.models import Book


def get_book_names(max_results=0, starts_with=''):
    names = []
    if starts_with:
        names = Book.objects.filter(title__istartswith=starts_with) | Book.objects.filter(title__istartswith="the "+starts_with)
    
    if max_results > 0:
        if len(names) > max_results:
            names = names[:max_results]
    
    return names