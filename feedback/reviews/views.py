from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

from .models import Review

from .forms import ReviewForm

# Create your views here.

# def index(request):
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
      
#         if form.is_valid():

#             # print(form.cleaned_data)

#             # review = Review(
#             #     username=form.cleaned_data['username'],
#             #     review_text=form.cleaned_data['review_text'],
#             #     rating=form.cleaned_data['rating']
#             # )

#             # review.save()
#             form.save()
#             return redirect('/thank-you/')

        
#     #     print(request.POST['username'])
#     #     return redirect('/thank-you/')
#     if request.method == 'GET':
#         form = ReviewForm()
#         return render(request, 'reviews/review.html',{'form': form})

# def thank_you(request):
#     return render(request,"reviews/thank.html")

class ThankYouView(TemplateView):
    template_name = "reviews/thank.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "This works!"
        return context




# basic class based view
class IndexView(ListView):
    model = Review
    template_name = "reviews/review.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return Review.objects.filter(rating__gt=5).order_by('-id')






    # def get(self,request):{{ reviews }}
        # form = ReviewForm()
        # return render(request, 'reviews/review.html',{'form': form})
        # reviews = Review.objects.all()
        # return render(request, 'reviews/review.html',{'reviews': reviews})


    # def post(self,request):
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #     return redirect('/thank-you/')

# template view
# list view - get all objects
# detailed view - get the details of a single object
# create view
# form view
# update view
# delete view



class ReviewView(FormView):
    template_name = "reviews/review.html"
    form_class = ReviewForm
    success_url = "/thank-you/"

    def form_valid(self, form):
        form.save()
        # print(form)
        return super().form_valid(form)
        
        

       
    







