from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    # ex: /books/
    path("", views.index, name="index"),
    # ex: /books/5/
    path("<int:book_id>/", views.detail, name="detail")
]