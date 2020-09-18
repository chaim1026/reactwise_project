from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:      
        model = Contact
        fields = '__all__'
        exclude = ['date']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'text': forms.Textarea(attrs={'class': 'materialize-textarea', 'placeholder': 'Message'})
        }