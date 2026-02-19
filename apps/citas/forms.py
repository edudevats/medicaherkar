from django import forms
from .models import Cita

class SolicitarCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_cita', 'motivo']
        widgets = {
            'fecha_cita': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe brevemente el motivo de tu consulta'}),
        }
