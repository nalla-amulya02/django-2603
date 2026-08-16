from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.
# def pizza(request):
#     return HttpResponse("pizza menu");

# def burger(request):
#     return HttpResponse("burger menu");

def recipe(request,item):
    return HttpResponse(item)

def index(request):
    return HttpResponse("Welcome to the recipe app")

def login(request,num):
    # return HttpResponseRedirect("https://www.google.com")
    # menu/1
    # menu/recipe/1
    # menu.recipe/2
    # url = reverse("detailed_recipie", args=[num])
    # return HttpResponseRedirect(url)
    return redirect("detailed_recipie", args=[num])









    # httpresponseredirect
    # reverse
    # return redirect("")