from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Blog.models import Post, Categoria

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user', 'user@mail.com', 'pass')
        self.cat = Categoria.objects.create(nombre='Tec')
        self.post = Post.objects.create(titulo='Test', contenido='Contenido', autor=self.user)
        self.post.categoria.add(self.cat)

    # ----------- home/lista ----------
    def test_blog_status_200(self):
        response = self.client.get(reverse('Blog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    # ----------- detalle ----------
    def test_detalle_post_200(self):
        url = reverse('detalle_post_url', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    def test_detalle_post_404(self):
        url = reverse('detalle_post_url', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # ----------- categoría ----------
    def test_vista_categoria_filtra_correcto(self):
        url = reverse('categoria', args=[self.cat.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

    # ----------- búsqueda ----------
    def test_busqueda_titulo(self):
        response = self.client.get(reverse('Blog'), {'buscar': 'Test'})
        self.assertContains(response, 'Test')

    def test_busqueda_sin_resultados(self):
        response = self.client.get(reverse('Blog'), {'buscar': 'xyz'})
        self.assertNotContains(response, 'Test')