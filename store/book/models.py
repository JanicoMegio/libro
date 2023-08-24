from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


BOOK_STATUS = (
    ('new', 'NEW'),
    ('sale', 'SALE'),
)


class Book(models.Model):
    title = models.CharField(max_length=255)
    book_author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(max_length=1000, null=True)
    published = models.DateField()  
    status = models.CharField(
        max_length=10, choices=BOOK_STATUS, default='new')
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

    def __str__(self):
        author_names = ' '.join([author.name for author in self.book_author.all()])
        return f"{self.title} by {author_names}"
