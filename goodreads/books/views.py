from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Max, Min

from .forms import BookForm, ReviewForm
from .models import Book, Review

def book_list(request):
    books_list= Book.objects.all()
    context = {"books_list": books_list}
    return render(request, "books/book_list.html", context)


def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    reviews = book.reviews.all()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews
    })

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

def review_create(request, id):
    book = get_object_or_404(Book, pk=id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = ReviewForm()
    return render(request, 'books/review_form.html', {'form': form, 'book': book})

def review_update(request, book_id, review_id):
    book = get_object_or_404(Book, pk=book_id)
    review = get_object_or_404(Review, pk=review_id, book=book)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = ReviewForm(instance=review)

    return render(request, 'books/review_form.html', {'form': form, 'book': book, 'review': review})

def review_delete(request, book_id, review_id):
    book = get_object_or_404(Book, pk=book_id)
    review = get_object_or_404(Review, pk=review_id, book=book)

    if request.method == 'POST':
        review.delete()
        return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))

    return render(request, 'books/review_delete.html', {'review': review, 'book': book})

def top_rated_books(request):
    # Get the top 10 books by average rating
    top_books = (
        Book.objects
        .annotate(avg_score=Avg('reviews__score'))
        .order_by('-avg_score')[:10]
    )
    for book in top_books:
        # Annotate highest and lowest review scores for each book
        book.highest_rated_review = book.reviews.order_by('-score').first()
        book.lowest_rated_review = book.reviews.order_by('score').first()

    return render(request, 'books/top_rated_books.html', {
        'top_books': top_books
    })