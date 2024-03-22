from django.test import TestCase
from bookle.models import Book
from django.urls import reverse
from bookle.forms import RegisterForm, ProfileEditForm, UserForm

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

class TestRegisterForm(TestCase):
   
    def test_register_form_is_invalid(self):
        form = RegisterForm(data={"email":"sophie@gmail..com", "bio":"This is my bio", "user_picture":""})
        self.assertFalse(form.is_valid())

class TestProfileEditForm(TestCase):

    def test_profile_edit_form_is_valid(self):
        form = ProfileEditForm(data={"bio": "Hi", "userpicture": "default.png" })
        self.assertTrue(form.is_valid)

class TestUserForm(TestCase):
    
    def test_user_form_is_valid(self):
        form = UserForm(data={"password": "bookle123"})
        self.assertTrue(form.is_valid)

class HomeViewTest(TestCase):

    def test_home_view(self):
          response = self.client.get(reverse('bookle:home'))
          self.assertEquals(response.status_code, 200)
          self.assertTemplateUsed(response, 'bookle/home.html')

class HomeViewTest(TestCase):

    def test_home_view(self):
          response = self.client.get(reverse('bookle:home'))
          self.assertEquals(response.status_code, 200)
          self.assertTemplateUsed(response, 'bookle/home.html')

class LoginViewTest(TestCase):

    def test_home_view(self):
          response = self.client.get(reverse('bookle:login'))
          self.assertEquals(response.status_code, 200)
          self.assertTemplateUsed(response, 'bookle/login.html')


