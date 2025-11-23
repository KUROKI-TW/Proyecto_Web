# forms.py
from django import forms
from .models import Post, Categoria 

class FormularioPost(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ['titulo', 'contenido', 'imagen', 'categoria']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
        }
