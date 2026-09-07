from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length= 20)
    rating = models.IntegerField()
    author = models.CharField(max_length= 20, default='NA')

    def __str__(self):
        return f"{self.title} ({self.rating})"





