from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Imagen

def bio(request):
    imagenes = Imagen.objects.all()
    return render(request, 'pages/bio.html', {'imagenes': imagenes})

def desbloquear_imagen(request, imagen_id):
    if request.method == 'POST':
        
        imagen = Imagen.objects.get(id=imagen_id)
        
        return JsonResponse({
            'status': 'ok',
            'imagen_url': imagen.imageurl,  
            'descripcion': imagen.descripcion  
        })
    return JsonResponse({'status': 'error'})

