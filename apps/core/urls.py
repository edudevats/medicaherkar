from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('nosotros/', views.NosotrosView.as_view(), name='nosotros'),
    path('especialidades/', views.EspecialidadesView.as_view(), name='especialidades'),
    path('instalaciones/', views.InstalacionesView.as_view(), name='instalaciones'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
]
