from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Author

def index(request):
    authors_list= Author.objects.order_by("-id")[:5]
    context = {"authors_list": authors_list}
    return render(request, "authors/index.html", context)


def detail(request, author_id):
    question = get_object_or_404(Author, pk=author_id)
    return render(request, "authors/detail.html", {"question": question})


# Assuming the data to be entered is presnet in these lists
# auth_name = ['Aman', 'Vijay', 'Jhon', 'Larry']
# auth_age = [timezone.now(), timezone.now(), timezone.now(), timezone.now()]
# auth_origin_country = ['Chile', 'USA', 'China', 'New Zeland']
# auth_description = ['a', 'b', 'c', 'd']


def add_author(request):
    return render(request, 'authors/add_author.html')

def process_author_addition(request):
    if request.method == 'POST':
        author_name = request.POST.get('name')
        author_date_birth = request.POST.get('date_birth')
        author_country_origin = request.POST.get('origin_country')
        author_description = request.POST.get('description')
        
        # Create a new patient entry in the database using the Patient model
        author = Author(name = author_name,
                        date_birth = author_date_birth,
                        origin_country = author_country_origin,
                        description = author_description)
        author.save()



        return HttpResponse("Data successfully inserted!")
    else:
        return HttpResponse("Invalid request method.")