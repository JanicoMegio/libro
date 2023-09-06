from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.models import User

from django.contrib import messages

#from django.contrib.auth.forms import UserCreationForm

#from .forms import LoginForm

from .models import Book, Author, Genre, CartItems, OrderedItems


from django.core.paginator import Paginator

#from django.conf import settings

#import stripe
from decimal import Decimal
# Create your views here.

def home(request):
    return HttpResponse('Working app here')


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user =  authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store-page/')
        else:
            print("error")
            messages.error(request, 'Invalid Login Credentials')
    return render(request, 'authentication/login.html')




def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, 'Create Successfully')
        else:
            messages.error(request, 'Password not match')

    return render(request, 'authentication/register.html')



# all book listing start here 

@login_required(login_url="login")
def store_page(request):
    user = request.user
    books = Book.objects.all()
    cart = CartItems.objects.filter(user_name=user).count()
    items_per_page = 12

    # Create a Paginator instance
    paginator = Paginator(books, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')   

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    context = {
        'page':page,
        'cart': cart,
    }
    
    return render(request, 'book/store_page.html', context=context)

@login_required(login_url="login")
def new_books(request):
    return render(request, 'book/new_books.html')



# end here 

@login_required(login_url="login")
def add_to_cart(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        current_user = request.user
        cart_item, created = CartItems.objects.get_or_create(user_name=current_user, book_title=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('book-detail', pk=pk)
    except Book.DoesNotExist:
        messages.error(request, 'Item not found!')
        return HttpResponse('Book not found!', status=404)


    

    
@login_required(login_url="login")
def view_cart(request):
    user = request.user
    items = CartItems.objects.filter(user_name=user)   
    total = sum(float(item.total_cart_items()) for item in items)
    context = {
        'items': items,
        'total':total,
    }
    return render(request, 'book/cart_page.html', context)




@login_required(login_url="login")
def cart_notif(request):
    user = request.user
    cart = CartItems.objects.filter(user_name=user).count()
    
    return JsonResponse({'cart':cart})




@login_required(login_url="login")
def minus_quantity(request, pk):
    #item_quantity = request.POST.get('quantity-input')
    item = get_object_or_404(CartItems, pk=pk)
    if item.quantity <= 1:
        messages.error(request, "Invalid")
        return redirect('view-cart')
    else:
        item.quantity -= 1
        item.save()
    
    return redirect('view-cart')




@login_required(login_url="login")
def plus_quantity(request, pk):
    #item_quantity = request.POST.get('quantity-input')
    item = get_object_or_404(CartItems, pk=pk)
    if item.quantity >= 100:
        messages.error(request, "Invalid")
        return redirect('view-cart')
    else:
        item.quantity += 1
        item.save()
    
    return redirect('view-cart')


@login_required(login_url="login")
def checkout_item(request):
    user = request.user
    user_cart = CartItems.objects.filter(user_name=user)
    total = sum(float(item.total_cart_items()) for item in user_cart)
    ordered_item, created = OrderedItems.objects.get_or_create(user_name=user, total=total )
    ordered_item.buy_items.set(user_cart)
    user_cart.delete()
    
    return redirect('payment-success')



@login_required(login_url="login")
def payment_success(request):
    return render(request, 'book/success.html')





# stripe.api_key = settings.STRIPE_API_KEY
# @login_required(login_url="login")
# @require_POST
# def create_checkout_session(request):
#     try:
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
        
#         user = request.user
#         book = OrderedItems.objects.filter(user_name=user)
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                     # Provide the exact Price ID (for example , pr_1234) of the product you want to sell
#                     'name':'{{ book }}',
#                     'price': '{{ book.total }}',
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success.html',
#             cancel_url=YOUR_DOMAIN + '/cancel.html',
#         )
#     except Exception as e:
#         return str(e)
    
#     return redirect(checkout_session.url, code=303)


@login_required(login_url="login")
def book_detail(request, pk):
    books = Book.objects.filter(pk=pk)
    return render(request, 'book/book_detail.html', {'books':books})




@login_required(login_url="login")
def delete_item_cart(request, pk):
    cart = CartItems.objects.filter(pk=pk)
    cart.delete()
    return redirect('view-cart')


@login_required(login_url="login")
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
    