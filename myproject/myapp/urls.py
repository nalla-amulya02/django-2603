from django.urls import path

from . import views


urlpatterns = [
    path('hello',views.home),

    # localhost:8080/myapp/
]
