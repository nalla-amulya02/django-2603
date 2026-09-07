from django.db import models

class Review(models.Model):

    username = models.CharField(max_length=100)

    review_text = models.TextField()

    rating = models.IntegerField()

    def __str__(self):
        return f"{self.username} - {self.rating}"