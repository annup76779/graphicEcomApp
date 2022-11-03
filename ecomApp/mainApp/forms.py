from django import forms
from mainApp.models import Graphics

class UploadGraphicsForm(forms.ModelForm):
    class Meta:
        model  = Graphics
        fields = ('title', "cost", "discount", "discription", "media")
        widgets = {
            "title" : forms.TextInput(attrs = {'class': 'form-control'}),
            'cost': forms.NumberInput(attrs = {'class': 'form-control'}),
            'discount': forms.NumberInput(attrs = {'class': 'form-control'}),
            'discription': forms.Textarea(attrs = {'class': 'form-control'})
        }