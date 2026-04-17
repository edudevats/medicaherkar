from django.urls import path
from . import views

app_name = 'especialistas'

urlpatterns = [
    path('', views.especialista_lista, name='lista'),
    path('<slug:slug>/', views.especialista_detalle, name='detalle'),
]
