from django import forms
from django.contrib.auth.hashers import make_password
from .models import Imagen, Registro

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['nombre', 'descripcion', 'imageurl', 'pregunta', 'respuesta', 'bloqueada']
        widgets = {
            'bloqueada': forms.CheckboxInput(),
        }

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['usuario', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control','id': 'password','required': True}),
            'usuario': forms.TextInput(attrs={'class': 'form-control','id': 'username','required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'email','required': True}),
        }

    def save(self, commit=True):
        registro = super().save(commit=False)
        registro.password = make_password(self.cleaned_data['password'])
        if commit:
            registro.save()
        return registro