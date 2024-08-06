from django.contrib import admin

from .models import Author, Book, Reviews, Sales

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Reviews)
admin.site.register(Sales)
