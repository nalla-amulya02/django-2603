from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
# Create your views here.

# [object(0),object(1)]
# # {
#     "id": 1,
#     "title": "Django Basics",
#     "author": "Amulya",
#     "price": 500,
#     "published_year": 2024
# }


from rest_framework.decorators import action, api_view
from rest_framework.response import Response

# from bookstore import books
from .models import Book
from .serializers import BookSerializer

# GET     /books/
# POST    /books/
# GET     /books/1/
# PUT     /books/1/
# PATCH   /books/1/
# DELETE  /books/1/


# Viewset
# @api_view(['GET'])
# def book_list(request):

#     books = Book.objects.all()

#     serializer = BookSerializer(books, many=True)

#     return Response(serializer.data)

class bookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#  api/books/expensive
    @action(detail=False, methods=['get'])
    def expensive(self, request):

        booksdata = Book.objects.filter(price__gt=20)
        print(booksdata)
        serializer = self.get_serializer(booksdata, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # //adding a custom action to the viewset
    # def create(self, request, *args, **kwargs):
    #     # //customization logic
    #     print("customization logic")
    #     return super().create(request, *args, **kwargs)

# api/books/1/author

    @action(detail=True, methods=['get'])
    def author(self, request, pk=None):
       
        return Response({
            "book_id": pk,
            "message": "Author information for this book"
        })




# list() get - api/books
# create() post - api/books
# retrieve() -  get api/books/pk
# update() - put api/books/pk
# partial_update() - patch api/books/pk
# destroy() - delete api/books/pk

# GET  api/books/expensive -> return all the books which are expensive (price > 20)