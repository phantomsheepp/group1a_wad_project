import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'group1a_wad_project.settings')

import requests
import django
django.setup()
from bookle.models import Book, Puzzle, UserProfile, Score, Comment


def fetch_books(keyword, max_results=20):
    results = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{keyword}").json()

    for item in results.get('items', []):
        # Extracting book details
        volume_info = item.get('volumeInfo', {})
        sales_info = item.get('saleInfo', {})

        authors = volume_info.get('authors', ['Unknown Author'])
        publishedDate = volume_info.get('publishedDate', '0000')
        categories = volume_info.get('categories', ['Unknown Genre'])

        # Simplify information extraction
        for identifier in volume_info.get('industryIdentifiers',[]):
            if identifier['type'] == "ISBN_13":
                isbn = identifier['identifier']
        title = volume_info.get('title', 'No Title')
        author = authors[0] if authors else 'Unknown Author'
        genre = categories[0] if categories else 'Unknown Genre'
        release_year = publishedDate.split('-')[0]
        country = sales_info.get('country', 'Unknown Country')
        description = volume_info.get('description', 'No Description')
        image_url = volume_info.get('imageLinks', {}).get('thumbnail')
        
        # Genre is a bit weird - might need removing
        # print(genre)

        if isbn != None:
            add_book(isbn, title, author, genre, release_year, country, description)

def populate():
    get_books_from_isbns(20)  

    puzzles = []

    for p in puzzles:
        add_puzzle(p['puzzleID'], p['date'], p['isbn'], p['difficulty'], p['popularity'])

def add_puzzle(puzzleID, date, isbn, difficulty=0, popularity=0):
    p = Puzzle.objects.get_or_create(puzzleID=puzzleID, date=date, isbn=isbn, 
                                     difficulty=difficulty, popularity=popularity)[0]
    p.save()
    return p

def add_book(isbn, title, author,genre, release_year, country, description):
    b = Book.objects.get_or_create(isbn=isbn, title=title)[0]
    b.author=author
    b.genre=genre
    b.release_year=release_year
    b.country=country
    b.description=description
    b.save()

def get_books_from_isbns(max=300):
    count = 0

    with open("isbns.txt","r") as file:
        for line in file:
            if count >= max:
                break

            isbn = fetch_books(line.strip(),1)
            count += 1


if __name__ == '__main__':
    print('Starting Rango population script...')  
    populate()
