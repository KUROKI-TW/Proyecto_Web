from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from Blog.models import Post

class PermissionTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.normal_user = User.objects.create_user('normal', 'n@mail.com', 'p')
        self.staff_user = User.objects.create_user('staff', 's@mail.com', 'p')
        
        # Asignar permiso explícitamente
        add_post_perm = Permission.objects.get(codename='add_post')
        self.staff_user.user_permissions.add(add_post_perm)
        self.staff_user.save()
        
        self.otro_user = User.objects.create_user('otro', 'o@mail.com', 'p')

    # ---- CREAR POST (solo usuarios con permiso) ----
    def test_anonimo_recibe_403(self):
        """Usuario anónimo recibe Forbidden (403)."""
        response = self.client.get(reverse('agregar_post'))
        self.assertEqual(response.status_code, 403)  # FORBIDDEN

    def test_usuario_sin_permiso_recibe_403(self):
        """Usuario sin permiso recibe Forbidden (403)."""
        self.client.login(username='normal', password='p')
        response = self.client.get(reverse('agregar_post'))
        self.assertEqual(response.status_code, 403)  # FORBIDDEN

    def test_usuario_con_permiso_puede_crear(self):
        """Usuario con permiso puede crear post."""
        self.client.login(username='staff', password='p')
        response = self.client.post(reverse('agregar_post'), {
            'titulo': 'Mi post',
            'contenido': 'Texto',
            'nueva_categoria': 'Personal'
        }, follow=True)
        self.assertRedirects(response, reverse('Blog'))
        self.assertTrue(Post.objects.filter(titulo='Mi post').exists())

    # ---- ELIMINAR POST (solo autor) ----
    def test_autor_puede_eliminar(self):
        """El autor del post puede eliminarlo."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.normal_user)
        self.client.login(username='normal', password='p')
        response = self.client.post(reverse('eliminar_post', args=[post.id]))
        self.assertEqual(Post.objects.filter(id=post.id).count(), 0)

    def test_no_autor_no_puede_eliminar(self):
        """Usuario que no es autor no puede eliminar."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.login(username='normal', password='p')
        self.client.post(reverse('eliminar_post', args=[post.id]))
        self.assertEqual(Post.objects.filter(id=post.id).count(), 1)

    # ---- EDITAR POST (solo autor) ----
    def test_autor_puede_editar(self):
        """El autor del post puede editar."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.normal_user)
        self.client.login(username='normal', password='p')
        response = self.client.get(reverse('editar_post', args=[post.id]))
        self.assertEqual(response.status_code, 200)

    def test_no_autor_no_puede_editar(self):
        """Usuario que no es autor es redirigido."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.login(username='normal', password='p')
        response = self.client.get(reverse('editar_post', args=[post.id]))
        self.assertEqual(response.status_code, 302)  # Redirige

    # ---- AJAX PERMISOS (IMPORTANTE: Usuario anónimo recibe 403) ----
    def test_usuario_autenticado_puede_dar_like(self):
        """Usuario autenticado puede dar like a cualquier post."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.login(username='normal', password='p')
        response = self.client.post(reverse('toggle_like', args=[post.id]), {
            'es_like': 'true'
        })
        self.assertEqual(response.status_code, 200)

    def test_usuario_anonimo_recibe_403_like(self):
        """Usuario anónimo recibe 403 en AJAX."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.logout()
        response = self.client.post(reverse('toggle_like', args=[post.id]))
        self.assertEqual(response.status_code, 403)  # FORBIDDEN

    def test_usuario_autenticado_puede_comentar(self):
        """Usuario autenticado puede comentar cualquier post."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.login(username='normal', password='p')
        response = self.client.post(reverse('agregar_comentario', args=[post.id]), {
            'contenido': 'Test'
        })
        self.assertEqual(response.status_code, 200)

    def test_usuario_anonimo_recibe_403_comentar(self):
        """Usuario anónimo recibe 403 en AJAX comentario."""
        post = Post.objects.create(titulo='P', contenido='C', autor=self.otro_user)
        self.client.logout()
        response = self.client.post(reverse('agregar_comentario', args=[post.id]))
        self.assertEqual(response.status_code, 403)  # FORBIDDEN
