import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'group1a_wad_project.settings')

import requests
import django
django.setup()
from bookle.models import Book, Puzzle, UserProfile, Score, Comment

def fetch_books(keyword, max_results=20):
    api_url = "https://www.googleapis.com/books/v1/volumes"
    books = []

    params = {
        'q': keyword,
        'maxResults': max_results,
        'printType': 'books',
        'orderBy': 'relevance'
    }

    response = requests.get(api_url, params=params)
    results = response.json()

    for item in results.get('items', []):
        # Extracting book details
        volume_info = item.get('volumeInfo', {})
        sales_info = item.get('saleInfo', {})

        authors = volume_info.get('authors', ['Unknown Author'])
        publishedDate = volume_info.get('publishedDate', '0000')
        categories = volume_info.get('categories', ['Unknown Genre'])

        # Simplify information extraction
        isbn = next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13'), None)
        title = volume_info.get('title', 'No Title')
        author = authors[0] if authors else 'Unknown Author'
        genre = categories[0] if categories else 'Unknown Genre'
        release_year = publishedDate.split('-')[0]
        country = sales_info.get('country', 'Unknown Country')
        description = volume_info.get('description', 'No Description')
        image_url = volume_info.get('imageLinks', {}).get('thumbnail')

        #print(type(isbn),type(title),type(author),type(genre),type(release_year),type(country),type(description))
        no_isbn=None
        if isbn == None:
            no_isbn = title
        else:
            Book.objects.get_or_create(isbn=isbn, title=title, author=author, genre=genre, release_year=release_year, country=country, description=description)
        
        return isbn, no_isbn

def populate():
    puzzles = []

    for p in puzzles:
        add_puzzle(p['puzzleID'], p['date'], p['isbn'], p['difficulty'], p['popularity'])

def add_puzzle(puzzleID, date, isbn, difficulty=0, popularity=0):
    p = Puzzle.objects.get_or_create(puzzleID=puzzleID, date=date, isbn=isbn, 
                                     difficulty=difficulty, popularity=popularity)[0]
    p.save()
    return p

def get_isbns():
    no_isbn = []
    with open("isbns.txt","w") as isbn_file:
        with open("books.txt","r") as title_file:
            for line in title_file:
                title = line.split("–")[0][:-1]
                isbn, title = fetch_books(title,1)
                if isbn != None:
                    isbn_file.write(isbn+"\n")
                else:
                    no_isbn.append(title)

    print(no_isbn)


if __name__ == '__main__':
    print('Starting Rango population script...')    
    populate()
