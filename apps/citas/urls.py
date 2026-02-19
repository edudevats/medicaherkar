from django.urls import path
from . import views

app_name = 'citas'

urlpatterns = [
    path('medicos/', views.ListaMedicosView.as_view(), name='lista_medicos'),
    path('solicitar/<int:medico_id>/', views.SolicitarCitaView.as_view(), name='solicitar_cita'),
    path('mis-citas/', views.MisCitasView.as_view(), name='mis_citas'),
    path('detalle/<int:pk>/', views.DetalleCitaView.as_view(), name='detalle_cita'),
]
