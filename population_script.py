import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'group1a_wad_project.settings')

import requests
import django
import datetime
import random
django.setup()
from django.contrib.auth.models import User
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
        release_year = int(publishedDate.split('-')[0])
        country = sales_info.get('country', 'Unknown Country')
        description = volume_info.get('description', 'No Description')
        cover = volume_info.get('imageLinks', {}).get('thumbnail')
        
        # Genre is a bit weird - might need removing
        # print(genre)

        if isbn != None:
            add_book(isbn, title, author, genre, release_year, country, description, cover)

def populate():
    get_books_from_isbns(15)  
    
    users = [{'username':"BookLuvr3", 'password':'secretBooks'},
             {'username':"bookle__xXx", 'password':'password1'},
             {'username':"lotr_is_my_fave", 'password':'123456'}]
    
    for u in users:
        add_user(u['username'], u['password'])

    puzzles = []
    for i in range(10):
        puzzles.append({'puzzleID':i+1,'isbn':Book.objects.all()[i],'date':datetime.date(2024,1,i+1), 'difficulty':round(random.uniform(0,5),2), 'popularity':round(random.uniform(0,5),2)})
    puzzles.append({'puzzleID':11,'isbn':Book.objects.all()[10],'date':datetime.date.today(), 'difficulty':round(random.uniform(0,5),2), 'popularity':round(random.uniform(0,5),2)})

    comments = [{'commentID':1, 'puzzleID': 11, 'user':User.objects.get(username="BookLuvr3"), 'comment':"Love this book!"},
                {'commentID':2, 'puzzleID': 11, 'user':User.objects.get(username="bookle__xXx"), 'comment':"tough puzzle today ://"},
                {'commentID':3, 'puzzleID': 11, 'user':User.objects.get(username="lotr_is_my_fave"), 'comment':"too EZ - hope tmrw's puzzle is harder!"},
                {'commentID':4, 'puzzleID': 3, 'user':User.objects.get(username="bookle__xXx"), 'comment':"THIS IS MY FAVOURITE BOOK"},
                {'commentID':5, 'puzzleID': 6, 'user':User.objects.get(username="lotr_is_my_fave"), 'comment':"i didn't like this book when i read it ..."}] 

    scores = [{'scoreID':1, 'puzzleID':11, 'user':User.objects.get(username="BookLuvr3"), 'guesses':4, 'difficulty':3, 'popularity':2},
              {'scoreID':2, 'puzzleID':11, 'user':User.objects.get(username="bookle__xXx"), 'guesses':2, 'difficulty':1, 'popularity':5},
              {'scoreID':3, 'puzzleID':11, 'user':User.objects.get(username="lotr_is_my_fave"), 'guesses':5, 'difficulty':5, 'popularity':1}]   

    for p in puzzles:
        puzzle = add_puzzle(p['puzzleID'], p['date'], p['isbn'], p['difficulty'], p['popularity'])

        for c in comments:
            if p['puzzleID'] == c['puzzleID']:
                add_comment(c['commentID'], puzzle, c['user'], c['comment'])

        for s in scores:
            if p['puzzleID'] == s['puzzleID']:
                add_score(s['scoreID'], s['user'], puzzle, s['guesses'], s['difficulty'], s['popularity'])


def add_puzzle(puzzleID, date, isbn, difficulty=0, popularity=0):
    p = Puzzle.objects.get_or_create(puzzleID=puzzleID, date=date, isbn=isbn)[0]
    p.difficulty=difficulty
    p.popularity=popularity
    p.save()
    return p

def add_book(isbn, title, author,genre, release_year, country, description, cover=''):
    b = Book.objects.get_or_create(isbn=isbn, title=title)[0]
    b.author=author
    b.genre=genre
    b.release_year=release_year
    b.country=country
    b.description=description
    b.cover=cover
    b.save()
    return b

def add_comment(commentID, puzzleID, userID, comment=""):
    c = Comment.objects.get_or_create(commentID=commentID, puzzleID=puzzleID, userID=userID)[0]
    c.comment=comment
    c.save()
    return c

def add_user(username, password):
    if not User.objects.filter(username=username):
        u = User.objects.create_user(username=username)
        u.set_password(password)
        u.save()
        return u

def add_score(scoreID, userID, puzzleID, guesses, difficulty=0, popularity=0):
    s = Score.objects.get_or_create(scoreID=scoreID, puzzleID=puzzleID, userID=userID)[0]
    s.guesses=guesses
    s.difficulty=difficulty
    s.popularity=popularity
    s.save()
    return s

def get_books_from_isbns(max=300):
    count = 0

    with open("isbns.txt","r") as file:
        for line in file:
            if count >= max:
                break

            isbn = fetch_books(line.strip(),1)
            count += 1


if __name__ == '__main__':
    print('Starting Bookle population script...')  
    populate()
