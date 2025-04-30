from django.db import models

class Imagen(models.Model):
    nombre = models.CharField(max_length=90)
    descripcion = models.CharField(max_length=2000)
    imageurl = models.CharField(max_length=120) 
    pregunta = models.CharField(max_length=2000)
    respuesta = models.CharField(max_length=2000)
    bloqueada = models.BooleanField(default=True)  # El bloqueo de la img

    def __str__(self):
        return self.nombre
    
class Registro(models.Model):
    usuario = models.CharField(max_length=90)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=2000)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario
