from django.contrib import admin
from django.utils.html import format_html
from .models import Especialidad, Especialista


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'icono')
    list_editable = ('orden',)
    prepopulated_fields = {'slug': ('nombre',)}
    ordering = ('orden',)


@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'publicado', 'orden', 'foto_preview')
    list_editable = ('publicado', 'orden')
    list_filter = ('publicado', 'especialidades')
    search_fields = ('nombre', 'cedula_profesional')
    filter_horizontal = ('especialidades',)
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ('creado', 'actualizado', 'foto_preview')

    def foto_preview(self, obj):
        if obj.foto:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="object-fit:cover;border-radius:50%;"/>',
                obj.foto.url,
            )
        return '—'
    foto_preview.short_description = 'Foto'
