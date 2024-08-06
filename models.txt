from django.db import models

class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    date_birth = models.DateField()
    origin_country = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name + " " + self.description


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    summary = models.TextField()
    date_of_pub = models.DateTimeField()
    num_sales = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.summary


class Reviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.CharField(max_length=200)
    review = models.TextField()
    score = models.IntegerField()
    num_upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.book + " " + self.review + " " + self.score


class Sales(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.CharField(max_length=200)
    sales = models.IntegerField(default=0)

    def __str__(self):
        return self.book + " " + self.sales
    