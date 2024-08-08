from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:author_id>/", views.author_detail, name="author_detail"),
    path("new/", views.author_create, name="author_create"),
    path('edit/<int:id>/', views.author_update, name='author_update'),
    path('delete/<int:id>/', views.author_delete, name='author_delete'),

    # path('author_list', views.author_list, name='author_list'),
]
