from django.shortcuts import render

def inicio(request):
    return render(request,"pages/index.html",{})

def login_view(request):
    return render(request, 'pages/login.html')

def registro_view(request):
    return render(request, 'pages/registro.html')

def admin_imagen_view(request):
    return render(request, 'pages/admin_imagen.html')