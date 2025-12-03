from django.test import TestCase
from django.contrib.auth.models import User
from Blog.models import Categoria, Post

class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@mail.com', 'pass')
        self.cat = Categoria.objects.create(nombre='Ciencia')

    def test_categoria_str(self):
        self.assertEqual(str(self.cat), 'Ciencia')

    def test_post_str(self):
        post = Post.objects.create(titulo='Título', contenido='Texto', autor=self.user)
        self.assertEqual(str(post), 'Título')

    def post_tiene_categoria(self):
        post = Post.objects.create(titulo='T', contenido='C', autor=self.user)
        post.categoria.add(self.cat)
        self.assertIn(self.cat, post.categoria.all())