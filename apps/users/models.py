from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    """
    Modelo de usuario personalizado para Clinica HerKar
    """

    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR = 'admin', 'Administrador'
        MEDICO = 'medico', 'Medico'
        PACIENTE = 'paciente', 'Paciente'

    # Eliminar username, usar email como identificador principal
    username = None
    email = models.EmailField('Correo electronico', unique=True)

    # Tipo de usuario
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TipoUsuario.choices,
        default=TipoUsuario.PACIENTE,
        verbose_name='Tipo de usuario'
    )

    # Campos comunes adicionales
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Telefono')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')

    # Control de registro
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_usuario_display()})"

    @property
    def es_admin(self):
        return self.tipo_usuario == self.TipoUsuario.ADMINISTRADOR

    @property
    def es_medico(self):
        return self.tipo_usuario == self.TipoUsuario.MEDICO

    @property
    def es_paciente(self):
        return self.tipo_usuario == self.TipoUsuario.PACIENTE


class PerfilMedico(models.Model):
    """
    Perfil adicional para usuarios tipo medico
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_medico',
        limit_choices_to={'tipo_usuario': User.TipoUsuario.MEDICO}
    )
    cedula_profesional = models.CharField(max_length=20, unique=True, verbose_name='Cedula profesional')
    especialidad = models.CharField(max_length=100, verbose_name='Especialidad')
    descripcion = models.TextField(blank=True, verbose_name='Descripcion')
    consultorio = models.CharField(max_length=50, blank=True, verbose_name='Consultorio')
    horario_atencion = models.TextField(blank=True, verbose_name='Horario de atencion')

    class Meta:
        verbose_name = 'Perfil de Medico'
        verbose_name_plural = 'Perfiles de Medicos'

    def __str__(self):
        return f"Dr. {self.usuario.get_full_name()} - {self.especialidad}"


class PerfilPaciente(models.Model):
    """
    Perfil adicional para usuarios tipo paciente
    """
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_paciente',
        limit_choices_to={'tipo_usuario': User.TipoUsuario.PACIENTE}
    )
    direccion = models.TextField(blank=True, verbose_name='Direccion')
    contacto_emergencia = models.CharField(max_length=100, blank=True, verbose_name='Contacto de emergencia')
    telefono_emergencia = models.CharField(max_length=20, blank=True, verbose_name='Telefono de emergencia')
    alergias = models.TextField(blank=True, verbose_name='Alergias')
    tipo_sangre = models.CharField(max_length=5, blank=True, verbose_name='Tipo de sangre')

    class Meta:
        verbose_name = 'Perfil de Paciente'
        verbose_name_plural = 'Perfiles de Pacientes'

    def __str__(self):
        return f"Paciente: {self.usuario.get_full_name()}"
