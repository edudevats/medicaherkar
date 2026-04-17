from django.shortcuts import render, get_object_or_404
from .models import Especialista


def especialista_lista(request):
    especialistas = (
        Especialista.objects
        .filter(publicado=True)
        .prefetch_related('especialidades')
        .order_by('orden', 'nombre')
    )
    return render(request, 'especialistas/lista.html', {'especialistas': especialistas})


def especialista_detalle(request, slug):
    especialista = get_object_or_404(Especialista, slug=slug, publicado=True)
    return render(request, 'especialistas/detalle.html', {'especialista': especialista})
