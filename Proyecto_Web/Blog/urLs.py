from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.post, name="Blog"),
    path('<int:post_id>/', views.detalle_post, name='detalle_post_url'),
    path('categoria/<int:categoria_id>/', views.categoria, name="categoria"),
    path('agregar/', views.AgregarPost, name='agregar_post'),
    path('editar/<int:post_id>/', views.EditarPost, name='editar_post'),
    path('eliminar/<int:post_id>/', views.EliminarPost, name='eliminar_post'),
    path('like/<int:post_id>/', views.ToggleLike, name='toggle_like'),  # NOMBRE CORRECTO
    path('comentario/<int:post_id>/', views.AgregarComentario, name='agregar_comentario'),  # NOMBRE CORRECTO
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)