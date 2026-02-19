from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Cita
from .forms import SolicitarCitaForm

User = get_user_model()

class ListaMedicosView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'citas/lista_medicos.html'
    context_object_name = 'medicos'

    def get_queryset(self):
        return User.objects.filter(
            tipo_usuario=User.TipoUsuario.MEDICO
        ).select_related('perfil_medico')

class SolicitarCitaView(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = SolicitarCitaForm
    template_name = 'citas/solicitar_cita.html'
    success_url = reverse_lazy('citas:mis_citas')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.medico = get_object_or_404(User, pk=self.kwargs['medico_id'], tipo_usuario=User.TipoUsuario.MEDICO)

    def form_valid(self, form):
        form.instance.paciente = self.request.user
        form.instance.medico = self.medico
        messages.success(self.request, 'Solicitud de cita enviada correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medico'] = self.medico
        return context

class MisCitasView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'citas/mis_citas.html'
    context_object_name = 'citas'

    def get_queryset(self):
        user = self.request.user
        if user.es_medico:
            return Cita.objects.filter(medico=user).order_by('fecha_cita')
        else:
            return Cita.objects.filter(paciente=user).order_by('fecha_cita')

class DetalleCitaView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cita
    template_name = 'citas/detalle_cita.html'
    context_object_name = 'cita'

    def test_func(self):
        cita = self.get_object()
        return self.request.user == cita.paciente or self.request.user == cita.medico
