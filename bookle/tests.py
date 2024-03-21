from django.test import TestCase
from bookle.models import Book

# Create your tests here.

class BookModelTest(TestCase):

  class BookModelTest(TestCase):
    def setUpTestData(self):
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

    def test_first_name_label(self):
        book = Book.objects.get(id=1)
        isbn = book.isbn
        self.assertEqual(isbn, 9780141345635)