from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView, UpdateView, DetailView, ListView,
    RedirectView, TemplateView
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import User, PerfilMedico, PerfilPaciente
from .forms import (
    LoginForm, RegistroPacienteForm, RegistroMedicoForm,
    EditarPerfilForm, EditarPerfilPacienteForm, EditarPerfilMedicoForm
)


# =============================================================================
# MIXINS DE PERMISOS
# =============================================================================

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere ser administrador"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_admin


class MedicoRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere ser medico"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_medico


class PacienteRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere ser paciente"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_paciente


# =============================================================================
# AUTENTICACION
# =============================================================================

class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('users:dashboard')


class LogoutView(auth_views.LogoutView):
    next_page = 'core:index'


class RegistroPacienteView(CreateView):
    """Auto-registro para pacientes"""
    model = User
    form_class = RegistroPacienteForm
    template_name = 'users/registro_paciente.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cuenta creada exitosamente. Ahora puede iniciar sesion.')
        return response


# =============================================================================
# DASHBOARDS
# =============================================================================

class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    """Redirige al dashboard segun tipo de usuario"""

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.es_admin:
            return reverse_lazy('users:dashboard_admin')
        elif user.es_medico:
            return reverse_lazy('users:dashboard_medico')
        else:
            return reverse_lazy('users:dashboard_paciente')


class DashboardAdminView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'users/dashboard_admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_medicos'] = User.objects.filter(
            tipo_usuario=User.TipoUsuario.MEDICO
        ).count()
        context['total_pacientes'] = User.objects.filter(
            tipo_usuario=User.TipoUsuario.PACIENTE
        ).count()
        context['medicos_recientes'] = User.objects.filter(
            tipo_usuario=User.TipoUsuario.MEDICO
        ).order_by('-fecha_registro')[:5]
        context['pacientes_recientes'] = User.objects.filter(
            tipo_usuario=User.TipoUsuario.PACIENTE
        ).order_by('-fecha_registro')[:5]
        return context


class DashboardMedicoView(LoginRequiredMixin, MedicoRequiredMixin, TemplateView):
    template_name = 'users/dashboard_medico.html'


class DashboardPacienteView(LoginRequiredMixin, PacienteRequiredMixin, TemplateView):
    template_name = 'users/dashboard_paciente.html'


# =============================================================================
# PERFIL
# =============================================================================

class PerfilView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user


class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditarPerfilForm
    template_name = 'users/editar_perfil.html'
    success_url = reverse_lazy('users:perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)


# =============================================================================
# GESTION DE MEDICOS (SOLO ADMIN)
# =============================================================================

class ListaMedicosView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/lista_medicos.html'
    context_object_name = 'medicos'

    def get_queryset(self):
        return User.objects.filter(
            tipo_usuario=User.TipoUsuario.MEDICO
        ).select_related('perfil_medico').order_by('-fecha_registro')


class CrearMedicoView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = User
    form_class = RegistroMedicoForm
    template_name = 'users/crear_medico.html'
    success_url = reverse_lazy('users:lista_medicos')

    def form_valid(self, form):
        messages.success(self.request, 'Medico creado exitosamente.')
        return super().form_valid(form)


class DetalleMedicoView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = User
    template_name = 'users/detalle_medico.html'
    context_object_name = 'medico'

    def get_queryset(self):
        return User.objects.filter(
            tipo_usuario=User.TipoUsuario.MEDICO
        ).select_related('perfil_medico')


class EditarMedicoView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = User
    template_name = 'users/editar_medico.html'
    fields = ['first_name', 'last_name', 'email', 'telefono', 'is_active']
    success_url = reverse_lazy('users:lista_medicos')

    def get_queryset(self):
        return User.objects.filter(tipo_usuario=User.TipoUsuario.MEDICO)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar formulario de perfil medico
        if self.object.es_medico and hasattr(self.object, 'perfil_medico'):
            context['perfil_form'] = EditarPerfilMedicoForm(instance=self.object.perfil_medico)
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Medico actualizado correctamente.')
        return super().form_valid(form)


# =============================================================================
# GESTION DE PACIENTES (SOLO ADMIN)
# =============================================================================

class ListaPacientesView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/lista_pacientes.html'
    context_object_name = 'pacientes'

    def get_queryset(self):
        return User.objects.filter(
            tipo_usuario=User.TipoUsuario.PACIENTE
        ).select_related('perfil_paciente').order_by('-fecha_registro')
