from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# we write views either in the form of function or classes

# function based views 
# class based views 

def home(request):
    return HttpResponse("Hello, World! This is my first Django project.")


