from django import forms

class ClassifyForm(forms.Form):
    url = forms.CharField(label="url",max_length=400)