from django.views.generic import TemplateView


class GatewayView(TemplateView):
    template_name = 'core/gateway.html'


class MedicosView(TemplateView):
    template_name = 'core/index.html'


class PacientesView(TemplateView):
    template_name = 'core/pacientes.html'


class IndexView(TemplateView):
    template_name = 'core/index.html'


class NosotrosView(TemplateView):
    template_name = 'core/nosotros.html'


class EspecialidadesView(TemplateView):
    template_name = 'core/especialidades.html'


class InstalacionesView(TemplateView):
    template_name = 'core/instalaciones.html'


class ContactoView(TemplateView):
    template_name = 'core/contacto.html'
