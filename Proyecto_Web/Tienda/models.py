from django.db import models
from django.contrib.auth.models import User

class CategoriaP(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    precio = models.FloatField()
    fotoP = models.ImageField(upload_to='tienda', null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    agregado = models.DateTimeField(auto_now_add=True)
    categoria = models.ManyToManyField(CategoriaP) 
    disponivilidad = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'


    def __str__(self):
        return self.nombre