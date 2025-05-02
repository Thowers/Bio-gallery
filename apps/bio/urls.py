from django.urls import path
from . import views
from .views import desbloquear_imagen
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.bio, name='bio'),
    path('desbloquear/<int:imagen_id>/', views.desbloquear_imagen, name='desbloquear_imagen'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




