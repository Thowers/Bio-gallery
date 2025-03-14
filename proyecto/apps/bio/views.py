from .models import Imagen

# Create your views here.
def imagenes(request):
    mis_imagenes = Imagen.objects.all()
    return render(request,"pages/imagenes.html",{"imagenes":mis_imagenes})