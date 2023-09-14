from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetails(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.TextField(max_length=1000)
    address2 = models.TextField(max_length=1000, blank=True, null=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    midname = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    birthdate = models.DateField(null=True)
    contact = models.CharField(max_length=11)

    def __str__(self):
        return f'Name:{self.lname}, {self.fname}. Details'



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
    image = models.ImageField(upload_to="book_images")
    genre = models.ManyToManyField(Genre)
    description = models.TextField(max_length=1000, null=True)
    published = models.DateField(null=True)
    status = models.CharField(
        max_length=10, choices=BOOK_STATUS, default='new')
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    review_star = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        author_names = ' '.join([author.name for author in self.book_author.all()])
        return f"{self.title} by {author_names}"
    


class CartItems(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_cart_items(self):
        return self.quantity * self.book_title.price
    
    def __str__(self):
        return f"item: {self.book_title} quantity: {self.quantity}"


ORDER_STATUS = (
    ('pending', 'PENDING'),
    ('order confirm', 'ORDER CONFIRM'),
    ('out of delivery', 'OUT OF DELIVERY'),
    ('delivered', 'DELIVERED'),
)

class Order(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    book_order = models.ForeignKey(Book, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_item = models.DecimalField(max_digits=10, decimal_places=2)
    review = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {self.book_order}"

class OrderedItems(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    buy_items = models.ManyToManyField(Order)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    item_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    received = models.BooleanField(default=False)
   
    
    def __str__(self):
        return f"Order_by: {self.user_name} total: {self.total} Date:{self.order_date}"


class CustomerReview(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    item_review = models.ForeignKey(Order, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    star = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Name: {self.user_name}, {self.item_review}"