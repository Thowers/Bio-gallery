# Crear archivo: biogallery/context_processors.py
from apps.bio.models import Registro

def auth_context(request):
    """Context processor para manejar autenticación personalizada"""
    context = {
        'user_authenticated': False,
        'current_user': None
    }
    
    if request.session.get('is_authenticated'):
        try:
            user_id = request.session.get('usuario_id')
            user = Registro.objects.get(id=user_id)
            context.update({
                'user_authenticated': True,
                'current_user': user,
                'user': user  # Para compatibilidad con {% if user.is_authenticated %}
            })
            # Crear un objeto mock user con is_authenticated
            class MockUser:
                def __init__(self, real_user):
                    self.username = real_user.usuario
                    self.email = real_user.email
                    self.id = real_user.id
                    self.is_authenticated = True
                    
            context['user'] = MockUser(user)
            
        except Registro.DoesNotExist:
            # Si el usuario no existe, limpiar sesión
            request.session.flush()
    
    return context