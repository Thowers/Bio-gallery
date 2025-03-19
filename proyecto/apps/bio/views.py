from django.shortcuts import render
from .models import Imagen

def bio(request):
    imagenes = Imagen.objects.all()
    return render(request, 'pages/bio.html', {'imagenes':imagenes})