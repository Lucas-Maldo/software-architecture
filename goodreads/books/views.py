from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import BookForm, ReviewForm
from .models import Book

def book_list(request):
    books_list= Book.objects.order_by("-id")[:5]
    context = {"books_list": books_list}
    return render(request, "books/book_list.html", context)

def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, "books/book_detail.html", {"book": book})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})


def book_update(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        book.delete()
        return HttpResponseRedirect(reverse("books:book_list"))
    return render(request, 'books/book_delete.html', {'book': book})