from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Username or password is incorrect')  
            return redirect('login_user')
        
    return render(request, 'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login_user')



# Create your views here.
