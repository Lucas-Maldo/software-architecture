from django.db import models
from django.db.models import Avg, Count, Sum

class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    date_birth = models.DateField()
    origin_country = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def number_of_books(self):
        return self.books.count()

    @property
    def average_score(self):
        return self.books.aggregate(Avg('reviews__score'))['reviews__score__avg'] or 0

    @property
    def total_sales(self):
        return self.books.aggregate(Sum('sales'))['sales__sum'] or 0