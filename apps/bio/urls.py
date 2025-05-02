from django.urls import path
from .views import bio, admin_imagen, desbloquear_imagen, admin_registro

app_name = 'bio'

urlpatterns = [
<<<<<<< HEAD
    path('', views.bio, name='bio'),
    path('desbloquear/<int:imagen_id>/', views.desbloquear_imagen, name='desbloquear_imagen'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('', bio, name='bio'),                                
    path('admin-imagen/', admin_imagen, name='admin_imagen'), 
    path('desbloquear-imagen/<int:imagen_id>/', desbloquear_imagen, name='desbloquear_imagen'),
]
>>>>>>> 7ba9fc7162394bee3009f519591ea37b7a907d6b




