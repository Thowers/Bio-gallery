from django.shortcuts import render, redirect
from django.contrib import messages
from apps.bio.forms import LoginForm
from apps.bio.models import Registro

def inicio(request):
    return render(request,"pages/index.html",{})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user_obj']
            # Guardar información del usuario en la sesión
            request.session['usuario_id'] = user.id
            request.session['usuario_nombre'] = user.usuario
            request.session['is_authenticated'] = True
            messages.success(request, f'¡Bienvenido {user.usuario}!')
            return redirect('/bio/')  # Redirigir a galería
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})

def registro_view(request):
    return render(request, 'pages/registro.html')

def admin_imagen_view(request):
    return render(request, 'pages/admin_imagen.html')

def logout_view(request):
    # Limpiar la sesión
    request.session.flush()
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('login')