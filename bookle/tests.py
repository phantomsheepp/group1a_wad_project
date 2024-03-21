from django.test import TestCase
from bookle.models import Book

# Create your tests here.

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(
            isbn=9780141345635,
            title='The Fault In Our Stars',
            author='John Green',
            genre='fiction',
            release_year='2014',
            country='US',
            cover='',
            description=''
        )

    def test_isbn_value(self):
        book = Book.objects.get(id=1)
        isbn = book.isbn
        self.assertEqual(isbn, '9780141345635')

    def test_author_value(self):
        book = Book.objects.get(id=1)
        author = book.author
        self.assertEqual(author, 'John Green')

    def test_country_value(self):
        book = Book.objects.get(id=1)
        country = book.country
        self.assertEqual(country, 'US')

