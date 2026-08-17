from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from django.template.loader import render_to_string

# Create your views here.
# def pizza(request):
#     return HttpResponse("pizza menu");

# def burger(request):
#     return HttpResponse("burger menu");

def recipe(request,item):
    # text = item + " recipe is available"
    # return HttpResponse(text)
    # text = "the recipe"
    # select recipe from items where item_name = item
    return render(request,"recipie/index.html", context = {"item":item})
# value - context data

# context -  dynamic info you send from view to template
# interpolate - how teh templates have tpo use /recieve the context data


def index(request):
    items = ["pizza","icecream","burger"]
    # html_data = render_to_string("recipie/index.html")
    # # return HttpResponse("Welcome to the recipe app")
    # return HttpResponse(html_data)
    return render(request,"recipie/index.html")

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