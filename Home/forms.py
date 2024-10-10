# forms.py
from django import forms

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=255, label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Message')
