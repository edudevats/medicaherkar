from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticacion
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Registro (solo pacientes pueden auto-registrarse)
    path('registro/', views.RegistroPacienteView.as_view(), name='registro'),

    # Dashboards segun tipo de usuario
    path('dashboard/', views.DashboardRedirectView.as_view(), name='dashboard'),
    path('dashboard/admin/', views.DashboardAdminView.as_view(), name='dashboard_admin'),
    path('dashboard/medico/', views.DashboardMedicoView.as_view(), name='dashboard_medico'),
    path('dashboard/paciente/', views.DashboardPacienteView.as_view(), name='dashboard_paciente'),

    # Perfil
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', views.EditarPerfilView.as_view(), name='editar_perfil'),

    # Gestion de medicos (solo admin)
    path('medicos/', views.ListaMedicosView.as_view(), name='lista_medicos'),
    path('medicos/nuevo/', views.CrearMedicoView.as_view(), name='crear_medico'),
    path('medicos/<int:pk>/', views.DetalleMedicoView.as_view(), name='detalle_medico'),
    path('medicos/<int:pk>/editar/', views.EditarMedicoView.as_view(), name='editar_medico'),

    # Gestion de pacientes (solo admin)
    path('pacientes/', views.ListaPacientesView.as_view(), name='lista_pacientes'),
]
