from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Post, Categoria

def validar_imagen(imagen):
    if imagen:
        if not imagen.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise ValidationError('Formato no permitido (jpg, jpeg, png, gif).')
        if imagen.size > 5 * 1024 * 1024:          # 5 MB
            raise ValidationError('Archivo mayor a 5 MB.')

class FormularioPost(forms.ModelForm):
    nueva_categoria = forms.CharField(
        max_length=30,
        required=False,
        label='O crea una nueva categoría',
        validators=[RegexValidator(r'^[\w\s]+$', 'Solo letras, números y espacios.')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Tecnología'
        })
    )

    imagen = forms.ImageField(
        required=False,
        validators=[validar_imagen],
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'imagen', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].required = False