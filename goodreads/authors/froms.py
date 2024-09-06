# forms.py
from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    date_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Author
        fields = ['name', 'date_birth', 'origin_country', 'description', 'image']
