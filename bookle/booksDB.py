import json
import requests
from bookle.models import Book

# class Book:
#     def __init__(self, title, author, genre, release_year, country):
#         self.title = title
#         self.author = author
#         self.genre = genre
#         self.release_year = release_year
#         self.country = country

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

        Book.objects.create(isbn=isbn, title=title, author=author, genre=genre, release_year=release_year, country=country, description=description)

        # Create a Book instance and add it to the list
    #     book = Book(title, author, genre, release_year, country)
    #     books.append(book)

    # return books


keywords = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for keyword in keywords:
    fetch_books(keyword)
# Example usage
# books_db = []
# keywords = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
# for keyword in keywords:
#     books = fetch_books(keyword)
#     books_db.extend(books)
