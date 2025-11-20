from django.urls import path
from .views import VRegistro, logaut, logear
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', VRegistro.as_view(),name="Autenticacion"),
    path('logaut', logaut,name="logaut"),
    path('logear', logear,name="logear"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)