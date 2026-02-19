from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha_cita', 'estado')
    list_filter = ('estado', 'fecha_cita', 'medico')
    search_fields = ('paciente__email', 'paciente__first_name', 'paciente__last_name', 'medico__email', 'medico__first_name', 'medico__last_name')
    date_hierarchy = 'fecha_cita'
