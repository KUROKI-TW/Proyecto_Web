from django.contrib import admin
from .models import Servicio

class ServiciosAmd(admin.ModelAdmin):
    list_display =('titulo','contenido','updated','imagen',)
    

admin.site.register(Servicio, ServiciosAmd,)


