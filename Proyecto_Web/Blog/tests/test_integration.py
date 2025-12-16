from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Blog.models import Post, Categoria, Like, Comentario

class IntegrationFlows(TestCase):

    def setUp(self):
        self.client = Client()
        
        # Usuario con permiso para crear posts
        self.autor = User.objects.create_user('victor', 'victor@mail.com', 'pass')
        add_perm = Permission.objects.get(codename='add_post')
        self.autor.user_permissions.add(add_perm)
        
        # Usuario normal sin permisos
        self.normal_user = User.objects.create_user('normal', 'n@mail.com', 'pass')
        
        self.post = Post.objects.create(
            titulo='Post Integración',
            contenido='Contenido completo',
            autor=self.autor
        )

    def test_flujo_completo_crear_post_con_categoria_nueva(self):
        """Flujo: Crear post con nueva categoría → Ver en lista → Dar like → Comentar."""
        self.client.login(username='victor', password='pass')
        
        # 1. Crear post con nueva categoría
        response = self.client.post(reverse('agregar_post'), {
            'titulo': 'Flujo Completo',
            'contenido': 'Contenido del flujo',
            'nueva_categoria': 'Integración'
        }, follow=True)
        self.assertRedirects(response, reverse('Blog'))
        
        # 2. Verificar que se creó la categoría
        self.assertTrue(Categoria.objects.filter(nombre='Integración').exists())
        
        # 3. Verificar que el post tiene la categoría
        post = Post.objects.get(titulo='Flujo Completo')
        self.assertIn('Integración', post.categoria.values_list('nombre', flat=True))
        
        # 4. Dar like como otro usuario
        self.client.login(username='normal', password='pass')
        like_response = self.client.post(reverse('toggle_like', args=[post.id]), {
            'es_like': 'true'
        })
        data = like_response.json()
        self.assertEqual(data['likes'], 1)
        
        # 5. Comentar como otro usuario
        comment_response = self.client.post(reverse('agregar_comentario', args=[post.id]), {
            'contenido': 'Comentario de integración'
        })
        self.assertTrue(comment_response.json()['success'])
        self.assertEqual(Comentario.objects.filter(post=post).count(), 1)

    def test_flujo_no_autor_no_puede_editar(self):
        """Flujo: Usuario normal intenta editar post de otro."""
        self.client.login(username='normal', password='pass')
        response = self.client.post(reverse('editar_post', args=[self.post.id]), {
            'titulo': 'Intento de edición',
            'contenido': 'Texto malicioso',
            'nueva_categoria': 'Hackeo'
        })
        # Debe redirigir sin editar
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.titulo, 'Intento de edición')

    def test_flujo_multiple_usuarios_likes(self):
        """Flujo: Varios usuarios dan like al mismo post."""
        # Crear usuarios adicionales
        user2 = User.objects.create_user('user2', 'u2@mail.com', 'pass')
        user3 = User.objects.create_user('user3', 'u3@mail.com', 'pass')
        
        # Cada usuario da like
        for user in [self.autor, user2, user3]:
            self.client.login(username=user.username, password='pass')
            self.client.post(reverse('toggle_like', args=[self.post.id]), {'es_like': 'true'})
            self.client.logout()
        
        # Verificar que se contabilizan 3 likes
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.filter(es_like=True).count(), 3)