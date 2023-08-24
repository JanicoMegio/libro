from django.shortcuts import render, redirect
from django.http import HttpResponse


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.contrib import messages

#from django.contrib.auth.forms import UserCreationForm

#from .forms import LoginForm

from .models import Book, Author, Genre

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


@login_required(login_url="login")
def store_page(request):
    books = Book.objects.all()
    return render(request, 'book/store_page.html', {'books':books})


@login_required(login_url="login")
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
    