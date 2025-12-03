from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .api import PostDetailAPI, PostListAPI

urlpatterns = [
    path('', views.post,name="Blog"),
    path('<int:post_id>/', views.detalle_post, name='detalle_post_url'),
    path('categoria/<int:categoria_id>/', views.categoria, name="categoria"),
    path('agregar/', views.AgregarPost, name='agregar_post'),
    path('eliminar/<int:post_id>/', views.EliminarPost, name='eliminar_post'),
    path('api/posts/', PostListAPI.as_view(), name='api_post_list'),
    path('api/posts/<int:pk>/', PostDetailAPI.as_view(), name='api_post_detail'),
    path('editar/<int:post_id>/', views.EditarPost, name='editar_post'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)