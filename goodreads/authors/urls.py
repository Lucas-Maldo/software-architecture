from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    # ex: /authors/
    path("", views.index, name="index"),
    # ex: /authors/5/
    path("<int:author_id>/", views.detail, name="detail"),
    # ex: /authors/add_author/
    path("add_author/", views.add_author, name="add_author"),
    # ex: /authors/add_author/
    path("process_author_addition/", views.process_author_addition, name="process_author_addition")
]