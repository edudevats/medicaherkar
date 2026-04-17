from django.db import migrations

ESPECIALIDADES = [
    ('Urología', 'urologia', 'fas fa-male', 1),
    ('Cirugía Plástica', 'cirugia-plastica', 'fas fa-star', 2),
    ('Otorrinolaringología', 'otorrinolaringologia', 'fas fa-head-side-mask', 3),
    ('Cirugía General', 'cirugia-general', 'fas fa-cut', 4),
    ('Ortopedia y Traumatología', 'ortopedia-y-traumatologia', 'fas fa-bone', 5),
    ('Ginecología', 'ginecologia', 'fas fa-female', 6),
]

DOCTOR_BIO = (
    'Me gradué de la Escuela de Medicina de la Universidad de Monterrey y realicé mi '
    'especialidad en cirugía general en el Hospital Christus Muguerza de Alta Especialidad '
    'en Monterrey. Posteriormente, me especialicé en cirugía plástica, estética y '
    'reconstructiva en el Hospital Central Militar de México y más adelante realicé un '
    'curso de alta especialización en cirugía estética en Miocorpo en la CDMX.\n\n'
    'Entiendo que hoy en día, lucir una figura armónica es una necesidad en nuestra '
    'sociedad, por eso me he especializado en tratamientos de cirugía de cara, cirugía '
    'de mama, cirugía reconstructiva, contorno corporal y procedimientos no quirúrgicos '
    'para rejuvenecer y embellecer la piel. Me apasiona mi trabajo y me comprometo con '
    'cada uno de mis pacientes para lograr los resultados que buscan.'
)

DOCTOR_AREAS = (
    'Cirugía de cara\n'
    'Cirugía de mama\n'
    'Cirugía reconstructiva\n'
    'Contorno corporal\n'
    'Procedimientos no quirúrgicos de rejuvenecimiento'
)


def seed(apps, schema_editor):
    Especialidad = apps.get_model('especialistas', 'Especialidad')
    Especialista = apps.get_model('especialistas', 'Especialista')

    especialidades = {}
    for nombre, slug, icono, orden in ESPECIALIDADES:
        esp = Especialidad.objects.create(
            nombre=nombre, slug=slug, icono=icono, orden=orden
        )
        especialidades[slug] = esp

    doctor = Especialista.objects.create(
        nombre='Dr. Ulises Caballero de la Peña',
        slug='ulises-caballero-de-la-pena',
        foto='especialistas/doc_ulises.jpg',
        cedula_profesional='8091368',
        cedula_especialidad='11656277',
        cmcper='2097',
        biografia=DOCTOR_BIO,
        universidad='Escuela de Medicina, Universidad de Monterrey',
        hospital_especialidad='Hospital Christus Muguerza de Alta Especialidad, Monterrey',
        areas_interes=DOCTOR_AREAS,
        orden=1,
        publicado=True,
    )
    doctor.especialidades.add(especialidades['cirugia-plastica'])


def reverse_seed(apps, schema_editor):
    Especialidad = apps.get_model('especialistas', 'Especialidad')
    Especialista = apps.get_model('especialistas', 'Especialista')
    Especialista.objects.filter(slug='ulises-caballero-de-la-pena').delete()
    slugs = [slug for _, slug, _, _ in ESPECIALIDADES]
    Especialidad.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('especialistas', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed, reverse_seed),
    ]
