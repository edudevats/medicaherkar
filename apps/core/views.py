from django.views.generic import TemplateView


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
