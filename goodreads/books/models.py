from django.db import models

from authors.models import Author

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    date_of_pub = models.DateTimeField()
    num_sales = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.summary

class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    score = models.IntegerField()
    num_upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.book + " " + self.review + " " + self.score


class Sale(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sales')
    year = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)

    def __str__(self):
        return self.book + " " + self.sales
    