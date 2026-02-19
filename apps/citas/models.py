from django.db import models
from django.conf import settings
from django.utils import timezone

class Cita(models.Model):
    class EstadoCita(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        CONFIRMADA = 'confirmada', 'Confirmada'
        CANCELADA = 'cancelada', 'Cancelada'
        REALIZADA = 'realizada', 'Realizada'

    paciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_solicitadas',
        limit_choices_to={'tipo_usuario': 'paciente'}
    )
    medico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citas_asignadas',
        limit_choices_to={'tipo_usuario': 'medico'}
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de solicitud')
    fecha_cita = models.DateTimeField(verbose_name='Fecha y hora de la cita')
    motivo = models.TextField(verbose_name='Motivo de la consulta')
    estado = models.CharField(
        max_length=20,
        choices=EstadoCita.choices,
        default=EstadoCita.PENDIENTE,
        verbose_name='Estado'
    )
    notas_medico = models.TextField(blank=True, verbose_name='Notas del medico')

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha_cita']

    def __str__(self):
        return f"Cita: {self.paciente} con {self.medico} - {self.fecha_cita.strftime('%d/%m/%Y %H:%M')}"
