from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Sum, F, Window
from django.db.models.functions import Rank
from django.core.cache import cache

from .documents import BookDocument



from .forms import BookForm, ReviewForm
from .models import Book, Review

def book_list(request):
    query = request.GET.get('search')

    books_list = cache.get('books')
    if not books_list:
        books_list = Book.objects.all()
        cache.set('books', books_list, 60*60*24)

    if query:
        try:
            title_search = BookDocument.search().query("match", name=query)
            summary_search = BookDocument.search().query("match", summary=query)
            books = title_search.to_queryset() | summary_search.to_queryset()
            books_list = books.distinct()
            print("Used elastic search")
        except Exception as e:
            print(e)
            books_list = Book.objects.filter(name__icontains=query) | Book.objects.filter(summary__icontains=query)
            print("Used database search")
    
    context = {"books_list": books_list}
    return render(request, "books/book_list.html", context)


def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    reviews = cache.get(f'book_reviews_{id}')
    if not reviews:
        reviews = book.reviews.all()
        cache.set(f'book_reviews_{id}', reviews, 60*60*24)


    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews
    })

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            cache.delete('books')
            cache.delete('top_books')
            cache.delete('top_selling_books')
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
            cache.delete('books')
            cache.delete('top_books')
            cache.delete('top_selling_books')
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = BookForm(instance=book)
        cache.delete('books')
        cache.delete('top_books')
        cache.delete('top_selling_books')
    return render(request, 'books/book_form.html', {'form': form})

def book_delete(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == "POST":
        book.delete()
        cache.delete('books')
        cache.delete('top_books')
        cache.delete('top_selling_books')
        return HttpResponseRedirect(reverse("books:book_list"))
    cache.delete('books')
    cache.delete('top_books')
    cache.delete('top_selling_books')
    return render(request, 'books/book_delete.html', {'book': book})

def review_create(request, id):
    book = get_object_or_404(Book, pk=id)
    
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            cache.delete(f'book_reviews_{id}')
            cache.delete('top_books')
            cache.delete('top_selling_books')
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = ReviewForm()
        cache.delete(f'book_reviews_{id}')
        cache.delete('top_books')
        cache.delete('top_selling_books')
    return render(request, 'books/review_form.html', {'form': form, 'book': book})

def review_update(request, book_id, review_id):
    book = get_object_or_404(Book, pk=book_id)
    review = get_object_or_404(Review, pk=review_id, book=book)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            cache.delete(f'book_reviews_{book_id}')
            cache.delete('top_books')
            cache.delete('top_selling_books')
            return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    else:
        form = ReviewForm(instance=review)
        cache.delete(f'book_reviews_{book_id}')
        cache.delete('top_books')
        cache.delete('top_selling_books')

    return render(request, 'books/review_form.html', {'form': form, 'book': book, 'review': review})

def review_delete(request, book_id, review_id):
    book = get_object_or_404(Book, pk=book_id)
    review = get_object_or_404(Review, pk=review_id, book=book)

    if request.method == 'POST':
        review.delete()
        cache.delete(f'book_reviews_{book_id}')
        cache.delete('top_books')
        cache.delete('top_selling_books')
        return HttpResponseRedirect(reverse("books:book_detail", args=(book.id,)))
    cache.delete(f'book_reviews_{book_id}')
    cache.delete('top_books')
    cache.delete('top_selling_books')
    return render(request, 'books/review_delete.html', {'review': review, 'book': book})

def top_rated_books(request):
    # Get the top 10 books by average rating
    top_books = cache.get('top_books')

    if not top_books:
        top_books = (
            Book.objects
            .annotate(avg_score=Avg('reviews__score'))
            .order_by('-avg_score')[:10]
        )
        for book in top_books:
            # Annotate highest and lowest review scores for each book
            book.highest_rated_review = book.reviews.order_by('-score').first()
            book.lowest_rated_review = book.reviews.order_by('score').first()
        cache.set('top_books', top_books, 60*60*24)

    return render(request, 'books/top_rated_books.html', {
        'top_books': top_books
    })

def top_selling_books(request):
    # Get the top 50 selling books
    top_selling_books = cache.get('top_selling_books')

    if not top_selling_books:
        top_selling_books = (
            Book.objects
            .annotate(total_sales=Sum('sales'))
            .order_by('-total_sales')[:50]
        )
        cache.set('top_selling_books', top_selling_books, 60*60*24)

    # Annotate total sales for each author
    for book in top_selling_books:
        author_total_sales = Book.objects.filter(author=book.author).aggregate(total_sales=Sum('sales'))['total_sales']
        book.author_total_sales = author_total_sales

        # Check if the book was among the top 5 selling books in its publication year
        year = book.date_of_pub.year
        top_books_in_year = (
            Book.objects
            .filter(date_of_pub__year=year)  # Use __year lookup for date fields
            .annotate(total_sales=Sum('sales'))
            .order_by('-total_sales')
        )

        # Annotate a ranking within its year
        ranked_books = top_books_in_year.annotate(rank=Window(
            expression=Rank(),
            partition_by=[F('date_of_pub__year')],
            order_by=F('total_sales').desc()
        ))
        book.rank_in_year = ranked_books.filter(id=book.id).first().rank

    return render(request, 'books/top_selling_books.html', {
        'top_books': top_selling_books,
    })