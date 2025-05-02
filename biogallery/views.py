from django.shortcuts import render, redirect.
from apps.bio.forms import LoginForm

def inicio(request):
    return render(request,"pages/index.html",{})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['usuario_id'] = form.cleaned_data['user_obj'].id
            return redirect('bio:bio')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})

def registro_view(request):
    return render(request, 'pages/registro.html')

def admin_imagen_view(request):
    return render(request, 'pages/admin_imagen.html')

