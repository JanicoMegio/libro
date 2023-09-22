from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseServerError


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.models import User

from django.contrib import messages

from django.db.models import Q

from django.db import transaction

#from django.contrib.auth.forms import UserCreationForm

from .forms import UserInfoForm, SortForm

from .models import Book, Author, Genre, CartItems, OrderedItems, UserDetails, Order, CustomerReview, Wishlist


from django.core.paginator import Paginator

#from django.conf import settings

#import stripe
from decimal import Decimal
# Create your views here.

def home(request):
    return HttpResponse('hello world')


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


# user account details 

@login_required(login_url="login")
def user_account(request):
    user = request.user
    persons = UserDetails.objects.filter(user_name=user)
    user_id = persons.first()
    context = {
        'persons': persons,
        'user_id':user_id
    }   
    return render(request, 'book/account.html', context=context)


@login_required(login_url="login")
def user_info(request):
    user_name = request.user
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        midname = request.POST['midname']
        age = request.POST['age']
        birthdate = request.POST['birthdate']
        contact = request.POST['contact']
        address1 = request.POST['address1']
        address2 = request.POST['address2']

        UserDetails.objects.create(user_name=user_name,
            fname=fname,
            lname=lname,
            midname=midname,
            age=age,
            contact=contact,
            birthdate=birthdate,
            address1=address1,
            address2=address2,

         )
        messages.success(request, 'Added Successfully.')
        return redirect('user-account')
    return render(request, 'book/create-info.html')




@login_required(login_url="login")
def update_user_info(request, pk):

    info = get_object_or_404(UserDetails, pk=pk)

    if request.method == "POST":
        info.fname = request.POST['fname']
        info.lname = request.POST['lname']
        info.midname = request.POST['midname']
        info.age = request.POST['age']
        info.birthdate = request.POST['birthdate']
        info.contact = request.POST['contact']
        info.address1 = request.POST['address1']
        info.address2 = request.POST['address2']

        info.save()
        return redirect('user-account')

    return render(request, 'book/update-info.html', {'info':info})



# all book listing start here 

@login_required(login_url="login")
def store_page(request):
    user = request.user
    book_new = Book.objects.all().order_by("-date")[:7]
    books = Book.objects.all().order_by("?")[:6]
    featured_author = Author.objects.all().order_by("?")[:1]
    genre = Genre.objects.all().order_by('?')[:6]
    trend = Book.objects.all().order_by('-review_star')[:6]

    items_per_page = 6

    # Create a Paginator instance
    paginator = Paginator(books, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')   

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    context = {
        #'page':page,
        'book_new':book_new,
        'books':books,
        'genre': genre,
        'trend': trend,
        #'cart': cart,
        #'rating':rating,
        'featured_author': featured_author,
    }
    
    return render(request, 'book/store_page.html', context=context)





@login_required(login_url="login")
def new_books(request):
    return render(request, 'book/new_books.html')



@login_required(login_url="login")
def wish_list(request):
    wish_list = Wishlist.objects.filter(user_name=request.user)
    context = {
    'wish_list':wish_list,
    }
    return render(request, 'book/wishlist.html', context)




@login_required(login_url="login")
def cart_notification(request):
    user = request.user
    cart = CartItems.objects.filter(user_name=user).count()

    response_data = {"cart":cart}

    return JsonResponse(response_data)

# end here 


#------------------------------------------------------- ADD TO CART FUNCTION

@login_required(login_url="login")
def add_to_cart(request, pk):
    book = Book.objects.get(pk=pk)
    current_user = request.user
    #cart = CartItems.objects.filter(user_name=current_user).count()
    try:
        cart_item, created = CartItems.objects.get_or_create(user_name=current_user, book_title=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
       
    except Book.DoesNotExist:
        messages.error(request, 'Item not found!')
    response_data = {'message': f'{book.title}'}
    return JsonResponse(response_data)
    
#-------------------------------------------------------- END HERE

@login_required(login_url="login")
def add_to_wishlist(request, pk):
    book = Book.objects.get(pk=pk)
    current_user = request.user
    try:
        wishlist, created = Wishlist.objects.get_or_create(user_name=current_user)
        wishlist.add_to_wishlist(book=book)
    except Book.DoesNotExist:
        messages.error(request, 'Item not found!')
    response_data = {'message': f'{book.title}'}
    return JsonResponse(response_data)


@login_required(login_url="login")
def add_to_cart_wishlist(request, pk):
    current_user = request.user
    book = Book.objects.get(pk=pk)
    wish_item = Wishlist.objects.get(user_name=current_user)
    try:
        cart_item, created = CartItems.objects.get_or_create(user_name=current_user, book_title=book)
        cart_item.save()
        wish_item.wish_book.remove(book)
        messages.success(request, f'{wish_item}')
    except Book.DoesNotExist:
        messages.error(request, 'Item not found!')
    return redirect('wishlist')


@login_required(login_url="login")
def wishlist_item_remove(request, pk):
    book = Book.objects.get(pk=pk)
    current_user = request.user
    wishlist = Wishlist.objects.get(user_name=current_user)
    wishlist.remove_from_wishlist(book=book)
    return redirect('wishlist')
    
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
    try:
        user = request.user
        user_cart_items = CartItems.objects.filter(user_name=user)
        
        if not user_cart_items.exists():
            return HttpResponse("Your cart is empty.")
        
        total = sum(float(item.total_cart_items()) for item in user_cart_items)
        
        # Use a transaction to ensure atomicity when creating orders and ordered items
        with transaction.atomic():
            # Create an order for each item in the cart
            orders = []
            for cart_item in user_cart_items:
                order, created = Order.objects.get_or_create(user_name=user, book_order=cart_item.book_title, qty=cart_item.quantity, total_item=cart_item.total_cart_items())
                order.save()
                orders.append(order)
            
            # Create or update the ordered items entry
            ordered_item, created = OrderedItems.objects.get_or_create(user_name=user, total=total)
            ordered_item.save()
            ordered_item.buy_items.set(orders)
        
        # Clear the user's cart after successfully checking out
        user_cart_items.delete()
        
        return redirect('payment-success')
    
    except Exception as e:
        # Handle exceptions gracefully
        return HttpResponseServerError(f"An error occurred: {str(e)}")



@login_required(login_url="login")
def user_order(request):
    user = request.user
    order_item = Order.objects.filter(user_name=user)
    order_details = OrderedItems.objects.filter(user_name=user, received=False) 
    user_details = UserDetails.objects.filter(user_name=user)
    #print(order_details)
    context = {
    'order_details': order_details,
    'order_item': order_item,
    'user_details': user_details,
    }

    return render(request, 'book/order.html', context=context)





@login_required(login_url="login")
def order_history(request):
    user = request.user
    reviewed_item = Order.objects.filter(user_name=user, review=False)
    user_review = CustomerReview.objects.filter(user_name=user).order_by('-date')
    order_list = OrderedItems.objects.filter(user_name=user, received=True)
    
    items_per_page = 2
    paginator = Paginator(user_review, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)


    context = {
    'reviewed_item': reviewed_item,
    'user_review': user_review,
    'order_list': order_list,
    'page': page,
    }
    return render(request, 'book/order_history.html', context)


       



@login_required(login_url="login")
def create_review(request, pk):
  
    order = get_object_or_404(Order, pk=pk)
    book = Book.objects.get(pk=order.book_order.id)
    if request.method == "POST":
        comment = request.POST.get('comment')
        rate = request.POST.get('rating')

      
        review, created = CustomerReview.objects.get_or_create(
            user_name=request.user,
            item_review=order,  
            comment=comment,
            star=rate
        )
        
        book.review_star += int(rate)
        order.review = True
        book.save()
        order.save()
        
        return redirect('order-history')

    context = {
        'order': order,
    }
    return render(request, 'book/create_review.html', context)


@login_required(login_url="login")
def item_received(request, pk):
    try:
        item = OrderedItems.objects.get(id=pk)
        item.received = True
        item.save()

    except OrderedItems.DoesNotExist:
        return HttpResponse("Error item does not exist")
    return redirect('order')





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
    user = request.user
    books = Book.objects.get(pk=pk)
    book_order_item = Order.objects.filter(book_order=pk).count()
    wish_item = Wishlist.objects.filter(user_name=user, wish_book=pk).first()
    genres = [genre_list.name for genre_list in books.genre.all()]
    cart = CartItems.objects.filter(user_name=user).count()
    related = Book.objects.filter(genre__name__in=genres).order_by("?")[:5]
    item_review = CustomerReview.objects.filter(item_review__book_order=pk).order_by("-date")[:3]
    context = {
    'books': books,
    'cart': cart,
    'wish_item': wish_item,
    'related': related,
    'book_order_item': book_order_item,
    'item_review': item_review,

    }
    return render(request, 'book/book_detail.html', context=context)



#-------------------------------------------- all book by genre -- start here 

def genre_novel(request):
    books = Book.objects.filter(genre__name="Novel")
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')

    genre = "Novel"
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }

    return render(request, 'book/by_category/novel.html', context)


def genre_romance(request):
    books = Book.objects.filter(genre__name="Romance").order_by("?")
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
    genre = "Romance"
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)



def genre_science(request):
    books = Book.objects.filter(genre__name__in="science").order_by("?")
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)


def genre_history(request):
    books = Book.objects.filter(genre__name__in="history").order_by("?")
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)



def shop_by_category(request, pk):
    genre = Genre.objects.get(pk=pk)
    books = Book.objects.filter(genre__name=genre).all()
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
    items_per_page = 12

    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)



#--------------------------------------------- all book by_category -- END HERE 

#--------------------------------------------- 3 SALE BANNER 

def sale_banner_1(request):
    books = Book.objects.all()
    genre = 'Online bundles'

    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
        
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)

def sale_banner_2(request):
    books = Book.objects.all()
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
    genre = 'Fave Reads'
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)

def sale_banner_3(request):
    books = Book.objects.all()
    sort_by = request.GET.get('sort_select')
    if sort_by == 'lth':
        books = books.order_by('price')
    elif sort_by == 'htl':
        books = books.order_by('-price')
    elif sort_by == 'bs':
        books = books.order_by('-review_star')
    elif sort_by == 'new':
        books = books.order_by('-date')
    genre = 'Special'
    items_per_page = 12
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
    'page': page,
    'genre': genre,
    'sort_by': sort_by,
    }
    return render(request, 'book/by_category/novel.html', context)


#--------------------------------------------- SALE BANNER --- END HERE 

#--------------------------------------------- SEACH ITEM -- START HERE 

def search_book(request):
    search_data = request.GET.get("search-item", "")
    sort_by = request.GET.get('sort_select')
    books_page = Book.objects.all()
    if search_data:
        books_page = books_page.filter(title__icontains=search_data)
    if sort_by == 'lth':
       books_page = books_page.order_by('price')
    elif sort_by == 'htl':
        books_page = books_page.order_by('-price')
    elif sort_by == 'bs':
        books_page = books_page.order_by('-review_star')
    elif sort_by == 'new':
        books_page = books_page.order_by('-date')


    result_count = books_page.count()
    paginator = Paginator(books_page, per_page=12)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'result_count': result_count,
        'search_data': search_data,
        'sort_by': sort_by, 
        }
    return render(request, 'book/by_category/search_item.html', context)
   
#--------------------------------------------- SEACH ITEM ----END HERE


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
    