from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, PerfilPaciente, PerfilMedico


class LoginForm(AuthenticationForm):
    """Formulario de login personalizado"""
    username = forms.EmailField(
        label='Correo electronico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Contrasena',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '********'
        })
    )


class RegistroPacienteForm(UserCreationForm):
    """Formulario de auto-registro para pacientes"""

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'telefono', 'fecha_nacimiento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = 'correo@ejemplo.com'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Juan'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Perez'
        self.fields['telefono'].widget.attrs['placeholder'] = '55 1234 5678'
        self.fields['fecha_nacimiento'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

        # Labels en espanol
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['password1'].label = 'Contrasena'
        self.fields['password2'].label = 'Confirmar contrasena'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = User.TipoUsuario.PACIENTE
        if commit:
            user.save()
            # Crear perfil de paciente automaticamente
            PerfilPaciente.objects.create(usuario=user)
        return user


class RegistroMedicoForm(UserCreationForm):
    """Formulario para registro de medicos (solo admin)"""
    cedula_profesional = forms.CharField(
        max_length=20,
        label='Cedula profesional',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    especialidad = forms.CharField(
        max_length=100,
        label='Especialidad',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['password1'].label = 'Contrasena'
        self.fields['password2'].label = 'Confirmar contrasena'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = User.TipoUsuario.MEDICO
        if commit:
            user.save()
            PerfilMedico.objects.create(
                usuario=user,
                cedula_profesional=self.cleaned_data['cedula_profesional'],
                especialidad=self.cleaned_data['especialidad']
            )
        return user


class EditarPerfilForm(forms.ModelForm):
    """Formulario para editar perfil de usuario"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'telefono', 'fecha_nacimiento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['fecha_nacimiento'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'


class EditarPerfilPacienteForm(forms.ModelForm):
    """Formulario para editar perfil adicional de paciente"""

    class Meta:
        model = PerfilPaciente
        fields = ['direccion', 'contacto_emergencia', 'telefono_emergencia', 'alergias', 'tipo_sangre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EditarPerfilMedicoForm(forms.ModelForm):
    """Formulario para editar perfil adicional de medico"""

    class Meta:
        model = PerfilMedico
        fields = ['cedula_profesional', 'especialidad', 'descripcion', 'consultorio', 'horario_atencion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
