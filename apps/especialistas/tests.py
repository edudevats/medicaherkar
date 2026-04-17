from django.test import TestCase
from django.urls import reverse


class EspecialidadModelTest(TestCase):
    def setUp(self):
        from apps.especialistas.models import Especialidad
        self.esp, _ = Especialidad.objects.get_or_create(
            slug='cirugia-plastica',
            defaults={
                'nombre': 'Cirugía Plástica',
                'icono': 'fas fa-star',
                'orden': 1,
            },
        )

    def test_str(self):
        self.assertEqual(str(self.esp), 'Cirugía Plástica')

    def test_ordering(self):
        from apps.especialistas.models import Especialidad
        esp2 = Especialidad.objects.create(nombre='Test B', slug='test-b-orden', icono='fas fa-b', orden=100)
        esp1 = Especialidad.objects.create(nombre='Test A', slug='test-a-orden', icono='fas fa-a', orden=99)
        nombres = list(Especialidad.objects.filter(slug__in=['test-a-orden', 'test-b-orden']).values_list('nombre', flat=True))
        self.assertEqual(nombres, ['Test A', 'Test B'])


class EspecialistaModelTest(TestCase):
    def setUp(self):
        from apps.especialistas.models import Especialidad, Especialista
        self.especialidad, _ = Especialidad.objects.get_or_create(
            slug='cirugia-plastica',
            defaults={'nombre': 'Cirugía Plástica', 'orden': 1},
        )
        self.doctor, _ = Especialista.objects.get_or_create(
            slug='ulises-caballero-de-la-pena',
            defaults={
                'nombre': 'Dr. Ulises Caballero de la Peña',
                'cedula_profesional': '8091368',
                'biografia': 'Bio de prueba.',
            },
        )
        self.doctor.especialidades.add(self.especialidad)

    def test_str(self):
        self.assertEqual(str(self.doctor), 'Dr. Ulises Caballero de la Peña')

    def test_get_absolute_url(self):
        expected = reverse('especialistas:detalle', kwargs={'slug': self.doctor.slug})
        self.assertEqual(self.doctor.get_absolute_url(), expected)

    def test_m2m_relation(self):
        self.assertIn(self.especialidad, self.doctor.especialidades.all())
        self.assertIn(self.doctor, self.especialidad.especialistas.all())

    def test_areas_interes_list(self):
        self.doctor.areas_interes = 'Cirugía de cara\nCirugía de mama'
        result = self.doctor.areas_interes_list()
        self.assertEqual(result, ['Cirugía de cara', 'Cirugía de mama'])

    def test_areas_interes_list_empty(self):
        self.doctor.areas_interes = ''
        self.assertEqual(self.doctor.areas_interes_list(), [])


class EspecialistaListaViewTest(TestCase):
    def setUp(self):
        from apps.especialistas.models import Especialista
        self.doctor_pub = Especialista.objects.create(
            nombre='Dr. Publicado',
            slug='dr-publicado',
            cedula_profesional='1111111',
            biografia='Bio.',
            publicado=True,
            orden=2,
        )
        self.doctor_no_pub = Especialista.objects.create(
            nombre='Dr. Oculto',
            slug='dr-oculto',
            cedula_profesional='2222222',
            biografia='Bio.',
            publicado=False,
            orden=1,
        )

    def test_lista_returns_200(self):
        response = self.client.get(reverse('especialistas:lista'))
        self.assertEqual(response.status_code, 200)

    def test_lista_only_published(self):
        response = self.client.get(reverse('especialistas:lista'))
        especialistas = list(response.context['especialistas'])
        self.assertIn(self.doctor_pub, especialistas)
        self.assertNotIn(self.doctor_no_pub, especialistas)

    def test_lista_respects_order(self):
        from apps.especialistas.models import Especialista
        doctor_orden_0 = Especialista.objects.create(
            nombre='Dr. Primero',
            slug='dr-primero',
            cedula_profesional='3333333',
            biografia='Bio.',
            publicado=True,
            orden=0,
        )
        response = self.client.get(reverse('especialistas:lista'))
        especialistas = list(response.context['especialistas'])
        self.assertEqual(especialistas[0], doctor_orden_0)


class EspecialistaDetalleViewTest(TestCase):
    def setUp(self):
        from apps.especialistas.models import Especialista
        self.doctor = Especialista.objects.create(
            nombre='Dr. Test',
            slug='dr-test',
            cedula_profesional='8091368',
            biografia='Bio.',
            publicado=True,
        )
        self.doctor_oculto = Especialista.objects.create(
            nombre='Dr. Oculto',
            slug='dr-oculto',
            cedula_profesional='9999999',
            biografia='Bio.',
            publicado=False,
        )

    def test_detalle_returns_200_for_published(self):
        response = self.client.get(
            reverse('especialistas:detalle', kwargs={'slug': 'dr-test'})
        )
        self.assertEqual(response.status_code, 200)

    def test_detalle_returns_404_for_unpublished(self):
        response = self.client.get(
            reverse('especialistas:detalle', kwargs={'slug': 'dr-oculto'})
        )
        self.assertEqual(response.status_code, 404)

    def test_detalle_returns_404_for_nonexistent_slug(self):
        response = self.client.get(
            reverse('especialistas:detalle', kwargs={'slug': 'no-existe'})
        )
        self.assertEqual(response.status_code, 404)
