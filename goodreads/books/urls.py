from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path("new/", views.book_create, name="book_create"),
    path('edit/<int:id>/', views.book_update, name='book_update'),
    path('delete/<int:id>/', views.book_delete, name='book_delete'),

    path('<int:id>/review/new/', views.review_create, name='review_create'),
    path('<int:book_id>/review/<int:review_id>/edit/', views.review_update, name='review_update'),
    path('<int:book_id>/review/<int:review_id>/delete/', views.review_delete, name='review_delete'),

    path('top-rated-books/', views.top_rated_books, name='top_rated_books'),
    path('top-selling-books/', views.top_selling_books, name='top_selling_books'),
]
