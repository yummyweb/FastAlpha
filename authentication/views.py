from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
import hashlib

# Create your views here.
def Register(request):
    if request.method == "POST":
        is_investor = None

        try:
            print(request.POST['is_investor'])
            is_investor = True
        except:
            is_investor = False

        user = User.objects.create(
            username=request.POST['username'], 
            email=request.POST['email'],
            is_investor=is_investor
        )
        user.set_password(request.POST['password'])
        user.save()
    return render(request, 'authentication/register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("Register")

    return render(request, 'authentication/login.html')

def UserPage(request, id):
    user = User.objects.get(id=id)

    context = {
        "user": user
    }

    return render(request, 'authentication/user.html', context)