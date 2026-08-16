from django.urls import path

from . import views


urlpatterns = [
    # path('pizza/',views.pizza),
    # path('burger/',views.burger),
    path("recipe/new/<int:item>",views.recipe, name = "detailed_recipie" ),
    path("", views.index, name = "index"),
    path("login/<int:num>", views.login, name=  " login ")

    

# localhost:8080/python-course
# str:
# int:
# slug: python-course
# uuid:
# path:

# syntax -> path(recipe/<variable>,view)
# localhost:8080/menu/recipe/1
# recipe 1
# localhost:8080/menu/recipe/2
# recipe 2
# localhost:8080/menu/recipe/3
# recipe 3

    # menu/1
    # menu/2
]
