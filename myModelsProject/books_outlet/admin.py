from django.contrib import admin
from .models import Book
# Register your models here.


class BooksAdmin(admin.ModelAdmin):
    list_display = ['title','rating','author','review']
    search_fields = ['title','author']
    list_filter = ['rating']
    ordering = ['rating']
    list_per_page = 3
    readonly_fields = ['title']

    def review(self,obj):
        if obj.rating >= 5:
            return 'Excellent'
        else:
            return "Avg"

admin.site.register(Book,BooksAdmin)

admin.site.site_header = "Library management system"
admin.site.site_title = "welcome librarian"
admin.site.index_title = "welcome"
