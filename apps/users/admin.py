from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PerfilMedico, PerfilPaciente


class PerfilMedicoInline(admin.StackedInline):
    model = PerfilMedico
    can_delete = False
    verbose_name = 'Perfil de Medico'
    verbose_name_plural = 'Perfil de Medico'


class PerfilPacienteInline(admin.StackedInline):
    model = PerfilPaciente
    can_delete = False
    verbose_name = 'Perfil de Paciente'
    verbose_name_plural = 'Perfil de Paciente'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'get_full_name', 'tipo_usuario', 'is_active', 'fecha_registro')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff', 'fecha_registro')
    search_fields = ('email', 'first_name', 'last_name', 'telefono')
    ordering = ('-fecha_registro',)

    # Campos para el formulario de edicion
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informacion Personal', {'fields': ('first_name', 'last_name',
                                              'telefono', 'fecha_nacimiento')}),
        ('Tipo de Usuario', {'fields': ('tipo_usuario',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                  'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos para el formulario de creacion
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'tipo_usuario',
                       'password1', 'password2'),
        }),
    )

    def get_inlines(self, request, obj=None):
        """Mostrar inline segun tipo de usuario"""
        if obj is None:
            return []
        if obj.tipo_usuario == User.TipoUsuario.MEDICO:
            return [PerfilMedicoInline]
        elif obj.tipo_usuario == User.TipoUsuario.PACIENTE:
            return [PerfilPacienteInline]
        return []


@admin.register(PerfilMedico)
class PerfilMedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cedula_profesional', 'especialidad', 'consultorio')
    list_filter = ('especialidad',)
    search_fields = ('usuario__email', 'usuario__first_name',
                     'cedula_profesional', 'especialidad')
    raw_id_fields = ('usuario',)


@admin.register(PerfilPaciente)
class PerfilPacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_sangre', 'contacto_emergencia')
    search_fields = ('usuario__email', 'usuario__first_name')
    raw_id_fields = ('usuario',)


# Personalizar titulo del admin
admin.site.site_header = 'Clinica HerKar - Administracion'
admin.site.site_title = 'Clinica HerKar Admin'
admin.site.index_title = 'Panel de Control'
