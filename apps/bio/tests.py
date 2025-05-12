import pytest
from django.urls import reverse
from apps.bio.models import Registro, Imagen
from django.contrib.auth.models import User

# Fixtures for registration and login tests
@pytest.fixture
def registro_data():
    return {
        'usuario': 'andres',
        'email': 'a@mail.com',
        'password': 'password123'
    }

@pytest.fixture
def existing_registro(db):
    return Registro.objects.create(usuario='andres', email='a@mail.com', password='password123')

@pytest.mark.django_db
class TestRegistroView:
    def test_formulario_registro_renderizado_correctamente(self, client):
        resp = client.get(reverse('admin_registro'))
        assert resp.status_code == 200
        assert '<form' in resp.content.decode()

    def test_registro_correcto(self, client, registro_data):
        resp = client.post(reverse('admin_registro'), data=registro_data)
        assert resp.status_code == 302
        assert Registro.objects.filter(usuario=registro_data['usuario']).exists()

    def test_registro_usuario_duplicado(self, client, existing_registro):
        data = {
            'usuario': existing_registro.usuario,
            'email': 'otro@mail.com',
            'password': 'password456'
        }
        resp = client.post(reverse('admin_registro'), data=data)
        assert resp.status_code == 200
        assert 'usuario ya existe' in resp.content.decode().lower()

    def test_registro_email_invalido(self, client):
        data = {'usuario': 'juan', 'email': 'noesemail', 'password': 'password123'}
        resp = client.post(reverse('admin_registro'), data=data)
        assert resp.status_code == 200
        assert 'correo electrónico inválido' in resp.content.decode().lower()

    def test_registro_con_campos_vacios(self, client):
        resp = client.post(reverse('admin_registro'), data={'usuario': '', 'email': '', 'password': ''})
        assert resp.status_code == 200
        assert 'este campo es obligatorio' in resp.content.decode().lower()

    def test_registro_con_contrasena_corta(self, client):
        data = {'usuario': 'corto', 'email': 'corto@mail.com', 'password': '12'}
        resp = client.post(reverse('admin_registro'), data=data)
        assert resp.status_code == 200
        assert 'al menos' in resp.content.decode().lower()

    def test_redireccion_despues_registro(self, client):
        data = {'usuario': 'mario', 'email': 'mario@mail.com', 'password': '123456789'}
        resp = client.post(reverse('admin_registro'), data=data)
        assert resp.status_code == 302
        assert resp.url.endswith(reverse('bio:bio'))

@pytest.mark.django_db
class TestLoginView:
    def test_login_correcto(self, client):
        # Creamos un registro y luego intentamos iniciar sesión
        Registro.objects.create(usuario='andres', email='a@mail.com', password='password123')
        resp = client.post(reverse('login'), data={'usuario': 'andres', 'password': 'password123'})
        assert resp.status_code == 302
        assert resp.url.endswith(reverse('bio:bio'))

    def test_login_contrasena_incorrecta(self, client):
        Registro.objects.create(usuario='andres', email='a@mail.com', password='password123')
        resp = client.post(reverse('login'), data={'usuario': 'andres', 'password': 'incorrecta'})
        assert resp.status_code == 200
        assert 'usuario o contrasena incorrectos' in resp.content.decode().lower()

    def test_login_usuario_inexistente(self, client):
        resp = client.post(reverse('login'), data={'usuario': 'noexiste', 'password': 'cualquiera'})
        assert resp.status_code == 200
        assert 'usuario o contrasena incorrectos' in resp.content.decode().lower()

@pytest.mark.django_db
class TestUnlockFlow:
    @pytest.fixture(autouse=True)
    def login_user(self, client):
        # Usamos un User estándar para la sesión
        user = User.objects.create_user(username='tester', password='secret123')
        client.login(username='tester', password='secret123')
        return user

    @pytest.fixture
    def imagen(db):
        return Imagen.objects.create(
            nombre="TestImg",
            descripcion="Descripción de prueba",
            imageurl="http://example.com/img.jpg",
            pregunta="¿2 + 2 es?",
            respuesta="4",
            bloqueada=True
        )

    def test_get_question_shows_pregunta(self, client, imagen):
        url = reverse('bio:desbloquear_imagen', args=[imagen.id])
        resp = client.get(url)
        assert imagen.pregunta.encode() in resp.content

    def test_post_correct_answer_unlocks_image(self, client, imagen):
        url = reverse('bio:desbloquear_imagen', args=[imagen.id])
        client.post(url, {'answer': '4'})
        imagen.refresh_from_db()
        assert not imagen.bloqueada

    def test_post_incorrect_answer_keeps_locked_and_shows_message(self, client, imagen):
        url = reverse('bio:desbloquear_imagen', args=[imagen.id])
        resp = client.post(url, {'answer': '5'})
        imagen.refresh_from_db()
        assert imagen.bloqueada
        assert b'incorrecto' in resp.content.lower()

