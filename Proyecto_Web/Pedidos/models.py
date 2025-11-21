from django.db import models
from django.contrib.auth import get_user_model
from Tienda.models import Producto
from django.db.models import F, Sum, FloatField

user = get_user_model()

class Pedido(models.Model):
    usuario= models.ForeignKey(user, on_delete= models.CASCADE)
    createdP = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pedido'
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['id']

    def __str__(self):
        return self.id
    

    @property
    def total(self):
        return self.lineaPedido_set.aggregate(
            total = Sum(F("precio")*F("cantidad"), output_file= FloatField())
        )["total"]

class LineaPedido(models.Model):
    usuario= models.ForeignKey(user, on_delete= models.CASCADE)
    producto= models.ForeignKey(Producto, on_delete= models.CASCADE)
    pedido= models.ForeignKey(Pedido, on_delete= models.CASCADE)
    cantidad = models.IntegerField(default=1)
    createdP = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.cantidad} unidades de {self.producto.nombre}'
    

    class Meta:
        db_table = 'lineaPedidos'
        verbose_name = 'lineaPedido'
        verbose_name_plural = 'lineaPedidos'
        ordering = ['id']