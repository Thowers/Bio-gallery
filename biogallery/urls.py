from django.contrib import admin
from django.urls import path, include
from .views import inicio, login_view, registro_view
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name="inicio"),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('bio/', include(('apps.bio.urls', 'bio'), namespace='bio')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)