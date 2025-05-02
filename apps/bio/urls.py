from django.urls import path.
from .views import bio, admin_imagen, desbloquear_imagen, admin_registro

app_name = 'bio'

urlpatterns = [
    path('', bio, name='bio'),                                
    path('admin-imagen/', admin_imagen, name='admin_imagen'), 
    path('desbloquear-imagen/<int:imagen_id>/', desbloquear_imagen, name='desbloquear_imagen'),
]




