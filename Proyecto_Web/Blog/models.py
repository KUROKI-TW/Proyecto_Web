from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.CharField(max_length=50000)
    imagen = models.ImageField(upload_to='blog', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # (1,M)
    categoria = models.ManyToManyField(Categoria) #(M,m)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


    def __str__(self):
            return self.titulo


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    es_like = models.BooleanField(default=True)  # True = like, False = dislike

    class Meta:
        unique_together = ('post', 'usuario')  # un voto por usuario

    def __str__(self):
        return f"{self.usuario} - {'👍' if self.es_like else '👎'}"


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"Comentario de {self.autor} en {self.post}"