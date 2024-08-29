from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.core.cache import cache

from .froms import AuthorForm
from .models import Author

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "authors/author_detail.html", {"author": author})    

def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            cache.delete('authors')
            return HttpResponseRedirect(reverse("authors:author_detail", args=(author.id,)))
    else:
        form = AuthorForm()
        cache.delete('authors')
    return render(request, 'authors/author_form.html', {'form': form})

def author_update(request, id):
    author = get_object_or_404(Author, pk=id)
    

    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            cache.delete('authors')
            return HttpResponseRedirect(reverse("authors:author_detail", args=(author.id,)))
    else:
        cache.delete('authors')
        form = AuthorForm(instance=author)
    return render(request, 'authors/author_form.html', {'form': form})

def author_delete(request, id):
    author = get_object_or_404(Author, pk=id)
    

    if request.method == "POST":
        author.delete()
        cache.delete('authors')
        return HttpResponseRedirect(reverse("authors:index"))
    cache.delete('authors')
    return render(request, 'authors/author_delete.html', {'author': author})

def index(request):
    authors = cache.get('authors')
    if not authors:
        authors = Author.objects.all()
        cache.set('authors', authors, 60*60*24)

    sort_by = request.GET.get('sort_by', 'name')
    filter_country = request.GET.get('filter_country', '')

    if filter_country:
        authors = authors.filter(country_of_origin__icontains=filter_country)

    if sort_by in ['name', 'number_of_books', 'average_score', 'total_sales']:
        if sort_by == 'number_of_books':
            authors = sorted(authors, key=lambda a: a.number_of_books, reverse=True)
        elif sort_by == 'average_score':
            authors = sorted(authors, key=lambda a: a.average_score, reverse=True)
        elif sort_by == 'total_sales':
            authors = sorted(authors, key=lambda a: a.total_sales, reverse=True)
        else:
            authors = authors.order_by(sort_by)
    
    return render(request, 'authors/index.html', {
        'authors': authors,
        'sort_by': sort_by,
        'filter_country': filter_country,
    })