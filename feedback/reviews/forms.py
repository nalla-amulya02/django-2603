from django import forms


# class ReviewForm(forms.Form):
#     username = forms.CharField(label='Your Name', max_length=100)
#     review_text = forms.CharField(
#         label='Your Feedback',
#         max_length=200,
#         widget=forms.Textarea
#     )
#     rating = forms.IntegerField(label = 'Rating', min_value=1, max_value=5)
    # review = forms.CharField(label='Your Review', widget=forms.Textarea)


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = "__all__"
        labels = {
            "username": "Your Name",
            "review_text": "Your Feedback",
            "rating": "Your Rating",
        }
        # fields =  ["username", "review_text","ratings"]
        


