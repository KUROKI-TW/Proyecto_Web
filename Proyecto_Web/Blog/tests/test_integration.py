from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Blog.models import Post, Categoria

class IntegrationFlows(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('autor', 'a@mail.com', 'p')
        self.user.user_permissions.add(
            Permission.objects.get(codename='add_post'),
            Permission.objects.get(codename='change_post')
        )

    def test_flujo_crear_post_y_aparece_en_lista(self):
        self.client.login(username='autor', password='p')
        cat = Categoria.objects.create(nombre='Novedades')
        response = self.client.post(reverse('agregar_post'), {
            'titulo': 'Nuevo post',
            'contenido': 'Contenido del post',
            'categoria': [cat.id]
        }, follow=True)
        self.assertRedirects(response, reverse('Blog'))
        self.assertContains(response, 'Nuevo post')

    def test_crear_post_con_nueva_categoria(self):
        self.client.login(username='autor', password='p')
        response = self.client.post(reverse('agregar_post'), {
            'titulo': 'Post con nueva cat',
            'contenido': 'Texto',
            'categoria': [],
            'nueva_categoria': 'Deportes'
        }, follow=True)
        self.assertRedirects(response, reverse('Blog'))
        self.assertTrue(Categoria.objects.filter(nombre='Deportes').exists())
        post = Post.objects.get(titulo='Post con nueva cat')
        self.assertIn('Deportes', post.categoria.values_list('nombre', flat=True))

    def test_editar_post_agrega_nueva_categoria(self):
        post = Post.objects.create(titulo='Original', contenido='Texto', autor=self.user)
        self.client.login(username='autor', password='p')
        response = self.client.post(reverse('editar_post', args=[post.id]), {
            'titulo': 'Editado',
            'contenido': 'Texto editado',
            'categoria': [],
            'nueva_categoria': 'Tecnología'
        }, follow=True)
        self.assertRedirects(response, reverse('detalle_post_url', args=[post.id]))
        post.refresh_from_db()
        self.assertIn('Tecnología', post.categoria.values_list('nombre', flat=True))