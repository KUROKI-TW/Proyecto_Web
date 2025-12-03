from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Blog.models import Post

class PermissionTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.normal_user = User.objects.create_user('normal', 'n@mail.com', 'p')
        self.otro_user = User.objects.create_user('otro', 'o@mail.com', 'p')

    # ---- CREAR POST ----
    def test_anonimo_redirige_a_login(self):
        response = self.client.get(reverse('agregar_post'))
        self.assertEqual(response.status_code, 302)  # redirige a login

    def test_usuario_autenticado_puede_ver_formulario(self):
        self.client.login(username='normal', password='p')
        response = self.client.get(reverse('agregar_post'))
        self.assertEqual(response.status_code, 200)

    def test_usuario_autenticado_puede_crear_post(self):
        self.client.login(username='normal', password='p')
        response = self.client.post(reverse('agregar_post'), {
            'titulo': 'Mi post',
            'contenido': 'Texto',
            'categoria': [],
            'nueva_categoria': 'Personal'
        }, follow=True)
        self.assertRedirects(response, reverse('Blog'))
        self.assertTrue(Post.objects.filter(titulo='Mi post').exists())
        self.assertTrue(Post.objects.get(titulo='Mi post').categoria.filter(nombre='Personal').exists())

    # ---- ELIMINAR POST ----
    def test_autor_puede_eliminar(self):
        post = Post.objects.create(titulo='P', contenido='C', autor=self.normal_user)
        self.client.login(username='normal', password='p')
        response = self.client.post(reverse('eliminar_post', args=[post.id]))
        self.assertEqual(Post.objects.filter(id=post.id).count(), 0)

    def test_no_autor_no_puede_eliminar(self):
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.login(username='normal', password='p')
        self.client.post(reverse('eliminar_post', args=[post.id]))
        self.assertEqual(Post.objects.filter(id=post.id).count(), 1)

    # ---- EDITAR POST ----
    def test_autor_puede_editar(self):
        post = Post.objects.create(titulo='P', contenido='C', autor=self.normal_user)
        self.client.login(username='normal', password='p')
        response = self.client.get(reverse('editar_post', args=[post.id]))
        self.assertEqual(response.status_code, 200)

    def test_no_autor_no_puede_editar(self):
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.login(username='normal', password='p')
        response = self.client.get(reverse('editar_post', args=[post.id]))
        self.assertEqual(response.status_code, 302)  # redirige
