from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Blog.models import Post, Like, Comentario


class AjaxLikeTests(TestCase):
    """Test para la funcionalidad de likes/dislikes vía AJAX."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('victor', 'victor@mail.com', 'pass123')
        self.post = Post.objects.create(
            titulo='Post de prueba',
            contenido='Contenido para testing',
            autor=self.user
        )
        self.client.login(username='victor', password='pass123')

    def test_usuario_puede_dar_like(self):
        """Verificar que un usuario autenticado puede dar like."""
        response = self.client.post(reverse('toggle_like', args=[self.post.id]), {
            'es_like': 'true'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['likes'], 1)
        self.assertEqual(data['dislikes'], 0)

    def test_usuario_puede_quitar_like(self):
        """Verificar que al dar like dos veces, se elimina el voto."""
        # Dar like
        self.client.post(reverse('toggle_like', args=[self.post.id]), {'es_like': 'true'})
        # Quitar like (segundo click)
        response = self.client.post(reverse('toggle_like', args=[self.post.id]), {
            'es_like': 'true'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['likes'], 0)  # Se eliminó

    def test_cambiar_de_like_a_dislike(self):
        """Verificar que se puede cambiar de like a dislike."""
        # Dar like primero
        self.client.post(reverse('toggle_like', args=[self.post.id]), {'es_like': 'true'})
        # Cambiar a dislike
        response = self.client.post(reverse('toggle_like', args=[self.post.id]), {
            'es_like': 'false'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['dislikes'], 1)

    def test_usuario_no_autenticado_es_redirigido(self):
        """Verificar que usuario anónimo es redirigido al login (302)."""
        self.client.logout()
        response = self.client.post(reverse('toggle_like', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # REDIRECCIÓN, no 403

    def test_metodo_get_no_permitido(self):
        """Verificar que solo se permite POST."""
        self.client.login(username='victor', password='pass123')
        response = self.client.get(reverse('toggle_like', args=[self.post.id]))
        self.assertEqual(response.status_code, 405)


class AjaxComentarioTests(TestCase):
    """Test para la funcionalidad de comentarios vía AJAX."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('victor', 'victor@mail.com', 'pass123')
        self.post = Post.objects.create(
            titulo='Post de prueba',
            contenido='Contenido para testing',
            autor=self.user
        )
        self.client.login(username='victor', password='pass123')

    def test_usuario_puede_comentar(self):
        """Verificar que un usuario autenticado puede añadir comentario."""
        response = self.client.post(reverse('agregar_comentario', args=[self.post.id]), {
            'contenido': 'Excelente post!'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['contenido'], 'Excelente post!')
        self.assertEqual(Comentario.objects.count(), 1)

    def test_comentario_vacio_no_permitido(self):
        """Verificar que no se aceptan comentarios vacíos."""
        response = self.client.post(reverse('agregar_comentario', args=[self.post.id]), {
            'contenido': ''
        })
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], 'Comentario vacío')

    def test_usuario_no_autenticado_es_redirigido(self):
        """Verificar que usuario anónimo es redirigido al login (302)."""
        self.client.logout()
        response = self.client.post(reverse('agregar_comentario', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)  # REDIRECCIÓN, no 403

    def test_metodo_get_no_permitido_comentario(self):
        """Verificar que solo se permite POST para comentarios."""
        self.client.login(username='victor', password='pass123')
        response = self.client.get(reverse('agregar_comentario', args=[self.post.id]))
        self.assertEqual(response.status_code, 405)