from django.shortcuts import render, get_object_or_404, redirect.
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import Imagen, Registro
from .forms import ImagenForm, RegistroForm

def bio(request):
    imagenes_list = Imagen.objects.all().order_by('id')
    paginator = Paginator(imagenes_list, 12)  # Muestra 10 imágenes por página
    
    page_number = request.GET.get('page')
    imagenes = paginator.get_page(page_number)
    
    return render(request, 'pages/bio.html', {'imagenes': imagenes})

@csrf_exempt  # Solo si tienes problemas con CSRF
def desbloquear_imagen(request, imagen_id):
    if request.method == 'POST':
        imagen = get_object_or_404(Imagen, id=imagen_id)
        imagen.bloqueada = False
        imagen.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def admin_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bio:bio')
    else:
        form = ImagenForm()
    return render(request, 'pages/admin_imagen.html', {'form': form})

def admin_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bio:bio')
    else:
        form = RegistroForm()
    return render(request, 'pages/registro.html', {'form': form})