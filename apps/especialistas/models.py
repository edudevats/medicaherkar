from django.db import models
from django.urls import reverse


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    descripcion_corta = models.CharField(max_length=255, blank=True)
    icono = models.CharField(max_length=64, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombre


class Especialista(models.Model):
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    foto = models.ImageField(upload_to='especialistas/', blank=True)
    cedula_profesional = models.CharField(max_length=20)
    cedula_especialidad = models.CharField(max_length=20, blank=True)
    cmcper = models.CharField(max_length=20, blank=True)
    biografia = models.TextField()
    universidad = models.CharField(max_length=200, blank=True)
    hospital_especialidad = models.CharField(max_length=200, blank=True)
    anios_experiencia = models.PositiveIntegerField(null=True, blank=True)
    areas_interes = models.TextField(
        blank=True,
        help_text='Un área de interés por línea.'
    )
    especialidades = models.ManyToManyField(
        Especialidad, related_name='especialistas', blank=True
    )
    orden = models.PositiveIntegerField(default=0)
    publicado = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('especialistas:detalle', kwargs={'slug': self.slug})

    def areas_interes_list(self):
        return [a.strip() for a in self.areas_interes.splitlines() if a.strip()]
