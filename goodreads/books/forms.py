from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    date_of_pub = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Book
        fields = ['name', 'summary', 'date_of_pub', 'num_sales', 'author']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'score', 'num_upvotes']

    score = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter a score between 1 and 5'})
    )