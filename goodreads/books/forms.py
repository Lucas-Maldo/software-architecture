from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    date_of_pub = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Book
        fields = ['name', 'summary', 'date_of_pub', 'num_sales']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'review', 'score', 'num_upvotes']
