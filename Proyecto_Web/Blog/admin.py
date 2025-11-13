from django.contrib import admin
from .models import Categoria, Post

class CategoriaAmd(admin.ModelAdmin):
    list_display = ('nombre','updated',) 
    

class PostAmd(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'autor')
    list_filter =('autor','categoria',)

admin.site.register(Categoria, CategoriaAmd,)

admin.site.register(Post, PostAmd,)
