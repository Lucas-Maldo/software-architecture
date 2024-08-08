from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse


from .froms import AuthorForm
from .models import Author

# def index(request):
#     authors_list = Author.objects.all()
#     context = {"authors_list": authors_list}
#     return render(request, "authors/index.html", context)


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, "authors/author_detail.html", {"author": author})    

def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return HttpResponseRedirect(reverse("authors:author_detail", args=(author.id,)))
    else:
        form = AuthorForm()
    return render(request, 'authors/author_form.html', {'form': form})

def author_update(request, id):
    author = get_object_or_404(Author, pk=id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author = form.save()
            return HttpResponseRedirect(reverse("authors:author_detail", args=(author.id,)))
    else:
        form = AuthorForm(instance=author)
    return render(request, 'authors/author_form.html', {'form': form})

def author_delete(request, id):
    author = get_object_or_404(Author, pk=id)
    if request.method == "POST":
        author.delete()
        return HttpResponseRedirect(reverse("authors:index"))
    return render(request, 'authors/author_delete.html', {'author': author})

def index(request):
    sort_by = request.GET.get('sort_by', 'name')
    filter_country = request.GET.get('filter_country', '')

    authors = Author.objects.all()

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