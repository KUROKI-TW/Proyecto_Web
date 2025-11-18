from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "carro"
urlpatterns = [
    path("agregar/<int:producto_id>", views.agregarP, name= "agregar"),
    path("eliminar/<int:producto_id>", views.eliminarP, name= "eliminar"),
    path("restar/<int:producto_id>", views.restarPro, name= "restar"),
    path("limpiar/<int:producto_id>", views.limpiarC, name= "limpiar"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)