from django.contrib import admin

from .models import Book, Review, Sale

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Sale)