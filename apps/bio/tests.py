import pytest
from django.urls import reverse
from apps.bio.models import Registro

@pytest.mark.django_db
class TestRegistroViewAndLogin:

    def test_registro_correcto(self, client):
        resp = client.post(reverse('admin_registro'), data={
            'usuario': 'andres',
            'email': 'a@mail.com',
            'password': 'password123'
        })
        assert resp.status_code == 302
        assert Registro.objects.filter(usuario='andres').exists()

    def test_login_correcto(self, client):
        Registro.objects.create(usuario='andres', email='a@mail.com', password='password123')
        resp = client.post(reverse('login'), data={
            'username': 'andres',
            'password': 'password123'
        })
        assert resp.status_code == 302
        assert resp.url.endswith(reverse('bio:bio'))

    def test_login_contraseña_incorrecta(self, client):
        Registro.objects.create(usuario='andres', email='a@mail.com', password='password123')
        resp = client.post(reverse('login'), data={
            'username': 'andres',
            'password': 'incorrecta'
        })
        assert resp.status_code == 200
        assert "Usuario o contrasena incorrectos" in resp.content.decode()

    def test_registro_usuario_duplicado(self, client):
        Registro.objects.create(usuario='andres', email='a@mail.com', password='password123')
        resp = client.post(reverse('admin_registro'), data={
            'usuario': 'andres',
            'email': 'otro@mail.com',
            'password': 'password456'
        })
        assert resp.status_code == 200
        assert "usuario ya existe" in resp.content.decode()

    def test_registro_email_invalido(self, client):
        resp = client.post(reverse('admin_registro'), data={
            'usuario': 'juan',
            'email': 'noesemail',
            'password': 'password123'
        })
        assert resp.status_code == 200
        assert "correo electrónico inválido" in resp.content.decode()

    def test_registro_con_campos_vacios(self, client):
        resp = client.post(reverse('admin_registro'), data={
            'usuario': '',
            'email': '',
            'password': ''
        })
        assert resp.status_code == 200
        assert "Este campo es obligatorio" in resp.content.decode()

    def test_registro_con_contraseña_corta(self, client):
        resp = client.post(reverse('admin_registro'), data={
            'usuario': 'corto',
            'email': 'corto@mail.com',
            'password': '12'
        })
        assert resp.status_code == 200
        assert "al menos" in resp.content.decode()

    def test_login_usuario_inexistente(self, client):
        resp = client.post(reverse('login'), data={
            'username': 'noexiste',
            'password': 'cualquiera'
        })
        assert resp.status_code == 200
        assert "Usuario o contrasena incorrectos" in resp.content.decode()

    def test_redireccion_despues_registro(self, client):
        resp = client.post(reverse('admin_registro'), data={
            'usuario': 'mario',
            'email': 'mario@mail.com',
            'password': '123456789'
        })
        assert resp.status_code == 302
        assert resp.url.endswith(reverse('bio:bio'))

    def test_formulario_registro_renderizado_correctamente(self, client):
        resp = client.get(reverse('admin_registro'))
        assert resp.status_code == 200
        assert "<form" in resp.content.decode()