from django.test import TestCase
from django.contrib.auth.models import User
from Blog.forms import FormularioPost
from Blog.models import Categoria, Post

class FormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('u', 'u@mail.com', 'p')
        self.cat = Categoria.objects.create(nombre='Gatos')

    def test_form_valido_con_categoria_existente_y_nueva_vacia(self):
        """Verificar que el formulario es válido con categoría existente y nueva_categoria vacía."""
        form = FormularioPost(data={
            'titulo': 'Título',
            'contenido': 'Contenido largo',
            'categoria': [self.cat.id],
            'nueva_categoria': ''
        })
        self.assertTrue(form.is_valid())

    def test_form_valido_con_nueva_categoria(self):
        """Verificar que el formulario es válido con nueva categoría."""
        form = FormularioPost(data={
            'titulo': 'Nuevo Título',
            'contenido': 'Contenido',
            'categoria': [],
            'nueva_categoria': 'Python'
        })
        self.assertTrue(form.is_valid())

    def test_form_sin_titulo_es_invalido(self):
        """Verificar que el título es obligatorio."""
        form = FormularioPost(data={
            'contenido': 'Sin título',
            'categoria': [],
            'nueva_categoria': 'Test'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)

    def test_nueva_categoria_con_caracteres_especiales_es_invalido(self):
        """Verificar que nueva_categoria rechaza caracteres especiales."""
        form = FormularioPost(data={
            'titulo': 'Test',
            'contenido': 'Texto',
            'categoria': [],
            'nueva_categoria': 'Python@!'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('nueva_categoria', form.errors)