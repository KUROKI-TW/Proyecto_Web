from django.contrib import admin
from .models import *

class PedidosAmd(admin.ModelAdmin):
    list_display = ('usuario','createdP',) 


class LineaPedidoAmd(admin.ModelAdmin):
    list_display = ('usuario', 'producto_id', 'pedido_id', 'cantidad','createdP',)
    list_filter =('usuario','producto_id','pedido_id',)


admin.site.register(Pedido, PedidosAmd,)
admin.site.register(LineaPedido, LineaPedidoAmd,)
