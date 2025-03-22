from django.db import models

class Imagen(models.Model):
    nombre = models.CharField(max_length=90)
    descripcion = models.CharField( max_length=2000)
    imageurl = models.URLField(max_length=500)
    pregunta = models.CharField( max_length=2000)
    respuesta = models.CharField( max_length=2000)
    
    def __str__(self):
        return self.nombre