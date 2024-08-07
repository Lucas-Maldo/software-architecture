from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    # ex: /authors/
    path("", views.index, name="index"),
    # ex: /authors/5/
    path("<int:author_id>/", views.author_detail, name="author_detail"),
    # ex: /authors/add_author/
    path("new/", views.author_create, name="author_create"),
    # ex: /authors/add_author/
    # path("process_author_addition/", views.process_author_addition, name="process_author_addition")
    path('edit/<int:id>/', views.author_update, name='author_update'),
    path('delete/<int:id>/', views.author_delete, name='author_delete'),
]