from django.contrib import admin
from .models import CategoriaP, Producto

class CategoriaPAmd(admin.ModelAdmin):
    list_display = ('nombre','updated',) 
    

class ProductoAmd(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'vendedor', 'agregado','precio','disponivilidad',)
    list_filter =('vendedor','categoria',)

admin.site.register(CategoriaP, CategoriaPAmd,)

admin.site.register(Producto, ProductoAmd,)