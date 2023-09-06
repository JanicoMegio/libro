from django.contrib import admin
from .models import Author, Genre, Book, CartItems, OrderedItems, UserDetails, CustomerReview
# Register your models here.

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(CartItems)
admin.site.register(OrderedItems)
admin.site.register(UserDetails)
admin.site.register(CustomerReview)