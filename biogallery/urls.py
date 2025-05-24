from django.contrib import admin
from django.urls import path, include
from .views import inicio, login_view
from apps.bio.views import admin_registro
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name="inicio"),  # Corregido: inicio en la raíz
    path('login/', views.login_view, name='login'),  # Corregido: login en /login/
    path('registro/', admin_registro, name='admin_registro'),
    path('logout/', views.logout_view, name='logout'),
    path('bio/', include(('apps.bio.urls', 'bio'), namespace='bio')),            
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)