from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ControlAccesoTests(TestCase):
    """Vistas públicas vs. privadas (FBV y CBV)."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('demo', password='Clave12345!')

    def test_bienvenida_es_publica(self):
        self.assertEqual(self.client.get(reverse('citas:home')).status_code, 200)

    def test_login_es_publico(self):
        self.assertEqual(self.client.get(reverse('citas:login')).status_code, 200)

    def test_cbv_protegidas_redirigen_a_login(self):
        for name in ('dashboard', 'medico_list', 'turno_list', 'turno_create', 'paciente_create'):
            url = reverse(f'citas:{name}')
            resp = self.client.get(url)
            self.assertRedirects(resp, f"{reverse('citas:login')}?next={url}")

    def test_fbv_protegida_redirige_a_login(self):
        url = reverse('citas:perfil')
        self.assertRedirects(self.client.get(url), f"{reverse('citas:login')}?next={url}")

    def test_usuario_autenticado_accede(self):
        self.client.login(username='demo', password='Clave12345!')
        for name in ('dashboard', 'medico_list', 'turno_list', 'perfil'):
            self.assertEqual(self.client.get(reverse(f'citas:{name}')).status_code, 200)

    def test_login_y_logout(self):
        resp = self.client.post(reverse('citas:login'), {'username': 'demo', 'password': 'Clave12345!'})
        self.assertRedirects(resp, reverse('citas:dashboard'), fetch_redirect_response=False)
        resp = self.client.post(reverse('citas:logout'))
        self.assertRedirects(resp, reverse('citas:home'), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse('citas:perfil')).status_code, 302)


class ApiPermisosTests(TestCase):
    def test_get_publico_y_post_requiere_login(self):
        self.assertEqual(self.client.get('/api/especialidades/').status_code, 200)
        resp = self.client.post('/api/especialidades/', {'nombre': 'X'}, content_type='application/json')
        self.assertEqual(resp.status_code, 403)

    def test_crud_autenticado(self):
        User.objects.create_user('demo', password='Clave12345!')
        self.client.login(username='demo', password='Clave12345!')
        r = self.client.post('/api/especialidades/', {'nombre': 'Neurología'}, content_type='application/json')
        self.assertEqual(r.status_code, 201)
        pk = r.json()['id']
        self.assertEqual(self.client.get(f'/api/especialidades/{pk}/').status_code, 200)
        self.assertEqual(self.client.patch(f'/api/especialidades/{pk}/', {'descripcion': 'a'}, content_type='application/json').status_code, 200)
        self.assertEqual(self.client.put(f'/api/especialidades/{pk}/', {'nombre': 'Neuro', 'descripcion': 'b'}, content_type='application/json').status_code, 200)
        self.assertEqual(self.client.delete(f'/api/especialidades/{pk}/').status_code, 204)
