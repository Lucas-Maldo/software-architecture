from django.db import models

class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    date_birth = models.DateField()
    origin_country = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

