from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "tienda" 

urlpatterns = [
    path('', views.tienda, name="tienda"),
    path('agregar/', views.AgregarProductos, name='agregar_productos'),
    path('eliminar/<int:producto_id>/', views.EliminarProducto, name='eliminar_producto'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)