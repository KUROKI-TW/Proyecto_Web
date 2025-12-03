from django.test import TestCase
from django.contrib.auth.models import User
from Blog.forms import FormularioPost
from Blog.models import Categoria, Post

class FormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('u', 'u@mail.com', 'p')
        self.cat = Categoria.objects.create(nombre='Gatos')

    def test_form_valido(self):
        form = FormularioPost(data={
            'titulo': 'Título',
            'contenido': 'Contenido largo',
            'categoria': [self.cat.id]
        })
        self.assertTrue(form.is_valid())

    def test_form_sin_titulo(self):
        form = FormularioPost(data={'contenido': 'Sin título'})
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)

    def test_nueva_categoria_no_requerida(self):
        form = FormularioPost(data={
            'titulo': 'Otro',
            'contenido': 'Texto',
            'categoria': []
        })
        self.assertTrue(form.is_valid())