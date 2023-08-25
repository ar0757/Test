from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='')
def index(request):
    return render(request, 'index.html')

@login_required(login_url='')
def homepage(request):
    return render(request,'layout/homepage.html')
# Create your views here.
