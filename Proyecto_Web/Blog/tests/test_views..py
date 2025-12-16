from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Blog.models import Post, Categoria, Like
from django.db.models import Count, Q

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('victor', 'victor@mail.com', 'pass')
        self.cat = Categoria.objects.create(nombre='Python')
        self.post = Post.objects.create(
            titulo='Test Post',
            contenido='Contenido de prueba',
            autor=self.user
        )
        self.post.categoria.add(self.cat)

    def test_blog_muestra_contadores_correctos(self):
        """Verificar que los contadores de likes se calculan correctamente."""
        # Dar like
        Like.objects.create(post=self.post, usuario=self.user, es_like=True)
        
        response = self.client.get(reverse('Blog'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar que el contador aparece en el template
        self.assertContains(response, 'id="likes-{}'.format(self.post.id))
        self.assertContains(response, 'id="dislikes-{}'.format(self.post.id))

    def test_detalle_post_muestra_comentarios(self):
        """Verificar que el detalle muestra lista de comentarios."""
        # Crear comentario
        self.client.login(username='victor', password='pass')
        self.client.post(reverse('agregar_comentario', args=[self.post.id]), {
            'contenido': 'Comentario de prueba'
        })
        
        response = self.client.get(reverse('detalle_post_url', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comentario de prueba')
        self.assertContains(response, '💬 Comentarios')

    def test_detalle_post_incluye_botones_compartir(self):
        """Verificar que el template incluye URLs de compartir."""
        response = self.client.get(reverse('detalle_post_url', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        
        # Verificar que las URLs de redes sociales están presentes
        self.assertContains(response, 'www.linkedin.com/sharing/share-offsite')
        self.assertContains(response, 'www.facebook.com/sharer/sharer.php')
        self.assertContains(response, 'twitter.com/intent/tweet')
        self.assertContains(response, 'wa.me/')

    def test_contadores_0_cuando_no_hay_votos(self):
        """Verificar que los contadores muestran 0 inicialmente."""
        response = self.client.get(reverse('Blog'))
        self.assertContains(response, '<span id="likes-{}">0</span>'.format(self.post.id))

    def test_optimizacion_de_queries(self):
        """Verificar que las vistas usan select_related y prefetch_related."""
        # Crear múltiples posts y likes para verificar N+1
        for i in range(5):
            post = Post.objects.create(
                titulo=f'Post {i}',
                contenido='Test',
                autor=self.user
            )
            Like.objects.create(post=post, usuario=self.user, es_like=True)
        
        # Si no hay N+1 problem, esto debe ejecutar pocas queries
        with self.assertNumQueries(5):  # Ajusta según tu optimización
            response = self.client.get(reverse('Blog'))
            self.assertEqual(response.status_code, 200)