from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Imagen

def bio(request):
    imagenes = Imagen.objects.all()
    return render(request, 'pages/bio.html', {'imagenes': imagenes})

def desbloquear_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)
    imagen.bloqueada = False
    imagen.save()
    return JsonResponse({'success': True})
