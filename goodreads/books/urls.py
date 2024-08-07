from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path("new/", views.book_create, name="book_create"),
    path('edit/<int:id>/', views.book_update, name='book_update'),
    path('delete/<int:id>/', views.book_delete, name='book_delete'),
]
