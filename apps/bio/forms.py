from django import forms
from django.contrib.auth.hashers import make_password, check_password
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

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if Registro.objects.filter(usuario__iexact=usuario).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return usuario

    def clean_email(self):
        email = self.cleaned_data['email']
        if Registro.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email
    
    def clean_password(self):
        pwd = self.cleaned_data.get('password', '')
        if len(pwd) < 8:
            raise forms.ValidationError("La contrasena debe tener al menos 8 caracteres.")
        return pwd

    def save(self, commit=True):
        registro = super().save(commit=False)
        registro.password = make_password(self.cleaned_data['password'])
        if commit:
            registro.save()
        return registro
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=90,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'required': True,
            'placeholder': 'Usuario'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'required': True,
            'placeholder': 'Contraseña'
        })
    )

    def clean(self):
        cleaned = super().clean()
        uname = cleaned.get('username')
        pwd   = cleaned.get('password')
        if uname and pwd:
            try:
                user = Registro.objects.get(usuario__iexact=uname)
            except Registro.DoesNotExist:
                raise forms.ValidationError("Usuario o contrasena incorrectos.")
            if not check_password(pwd, user.password):
                raise forms.ValidationError("Usuario o contrasena incorrectos.")
            cleaned['user_obj'] = user
        return cleaned