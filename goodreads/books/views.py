from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Book

def index(request):
    books_list= Book.objects.order_by("-id")[:5]
    context = {"books_list": books_list}
    return render(request, "books/index.html", context)

def detail(request, book_id):
    question = get_object_or_404(Book, pk=book_id)
    return render(request, "books/detail.html", {"question": question})
