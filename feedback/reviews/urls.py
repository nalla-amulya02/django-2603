from django.urls import path

from reviews import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view()),
    path('thank-you/',views.ThankYouView.as_view()),
]