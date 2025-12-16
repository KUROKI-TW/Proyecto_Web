from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Post, Categoria, Comentario

def validar_imagen(imagen):
    if imagen:
        if not imagen.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise ValidationError('Formato no permitido (jpg, jpeg, png, gif).')
        if imagen.size > 5 * 1024 * 1024:
            raise ValidationError('Archivo mayor a 5 MB.')

class FormularioPost(forms.ModelForm):
    # Campo único para crear/ingresar categoría
    nueva_categoria = forms.CharField(
        max_length=30,
        required=True,  # Obligatorio porque es el único campo de categoría
        label='Categoría del post',
        help_text='Escribe el nombre de la categoría (se creará automáticamente si no existe)',
        validators=[RegexValidator(r'^[\w\s]+$', 'Solo letras, números y espacios.')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Python, Web Dev, IA...'
        })
    )

    imagen = forms.ImageField(
        required=False,
        validators=[validar_imagen],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'imagen']  # Excluimos 'categoria'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
        }

class FormularioComentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Escribe tu comentario...'
            })
        }