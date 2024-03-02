import json
import requests

class Book:
    def __init__(self, title, author, genre, release_year, country):
        self.title = title
        self.author = author
        self.genre = genre
        self.release_year = release_year
        self.country = country



def fetch_books(keyword, max_results=20):
    api_url = "https://www.googleapis.com/books/v1/volumes"
    books = []

    params = {
        'q': keyword,
        'maxResults': max_results,
        'printType': 'books'
    }

    response = requests.get(api_url, params=params)
    results = response.json()

    for item in results.get('items', []):
        # Extracting book details
        volume_info = item.get('volumeInfo', {})
        title = volume_info.get('title', 'No Title')
        authors = volume_info.get('authors', ['Unknown Author'])
        publishedDate = volume_info.get('publishedDate', '0000')
        categories = volume_info.get('categories', ['Unknown Genre'])

        sales_info = item.get('saleInfo', {})
        country = sales_info.get('country', 'Unknown Country')

        # Simplify information extraction
        author = authors[0] if authors else 'Unknown Author'
        genre = categories[0] if categories else 'Unknown Genre'
        release_year = publishedDate.split('-')[0]

        # Create a Book instance and add it to the list
        book = Book(title, author, genre, release_year, country)
        books.append(book)

    return books

# Example usage
keyword = "Moby Dick"
books_db = fetch_books(keyword)
print(len(books_db))
# To demonstrate that books are fetched and stored in books_db
for book in books_db[:5]:  # Just show first 5 books for brevity
    print(book.title, "-", book.author, "-", book.genre, "-", book.release_year, "-", book.country)
