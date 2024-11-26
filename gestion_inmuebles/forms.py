from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TipoUsuario

class ExtendedUserCreationForm(UserCreationForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.all(),
        required=True,
        label="Tipo de Usuario",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rut = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'tipo_usuario', 'nombre', 'apellido', 'rut', 'direccion', 'telefono', 'correo')


from django import forms
from .models import Inmueble

# This is the final, single definition for CreateInmuebleForm
class CreateInmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'tipo_inmueble', 'comuna', 'region', 'nombre_inmueble', 'descripcion', 
            'm2_construido', 'numero_banos', 'numero_hab', 'direccion', 
            'numero_estacionam', 'image'  # Include image field
        ]
        widgets = {
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'nombre_inmueble': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'm2_construido': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_banos': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_hab': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_estacionam': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})  # Add file input widget
        }

from django import forms
from .models import Inmueble

class UpdateInmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'tipo_inmueble', 'comuna', 'region', 'nombre_inmueble',
            'descripcion', 'm2_construido', 'numero_banos',
            'numero_hab', 'direccion', 'numero_estacionam', 'image'
        ]
        widgets = {
            'comuna': forms.Select(attrs={'class': 'form-control'}),  # Ensures comuna is a dropdown
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # Image input widget
        }


from django import forms
from .models import PerfilUsuario

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'correo']
