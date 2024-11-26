from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Inmueble, PerfilUsuario,Solicitud
from .forms import ExtendedUserCreationForm


from django.shortcuts import render
from .models import Inmueble, Region, Comuna, TipoInmueble
from django.db.models import Q

def homepage(request):
    # Capture filter parameters from the request
    region_filter = request.GET.get('region', None)
    comuna_filter = request.GET.get('comuna', None)
    tipo_inmueble_filter = request.GET.get('tipo_inmueble', None)

    # Start with all inmuebles
    inmuebles = Inmueble.objects.select_related('tipo_inmueble', 'comuna', 'region', 'propietario__user')

    # Apply filters if the parameters are passed
    if region_filter:
        inmuebles = inmuebles.filter(region__id=region_filter)

    if comuna_filter:
        inmuebles = inmuebles.filter(comuna__id=comuna_filter)

    if tipo_inmueble_filter:
        inmuebles = inmuebles.filter(tipo_inmueble__id=tipo_inmueble_filter)

    # Get all possible filter options to display in the filter form
    regions = Region.objects.all()
    comunas = Comuna.objects.all()
    tipo_inmuebles = TipoInmueble.objects.all()

    # Render the template with the filtered inmuebles and filter options
    return render(request, 'homepage.html', {
        'inmuebles': inmuebles,
        'regions': regions,
        'comunas': comunas,
        'tipo_inmuebles': tipo_inmuebles
    })


@login_required
def dashboard(request):
    perfil = PerfilUsuario.objects.select_related('tipo_usuario').get(user=request.user)
    user_type = perfil.tipo_usuario.tipo_usuario  # Determine if the user is an arrendador or arrendatario

    if user_type == 'arrendador':
        inmuebles = Inmueble.objects.filter(propietario=perfil)
        solicitudes = Solicitud.objects.filter(inmueble__propietario=perfil)
    else:  # arrendatario
        inmuebles = None
        solicitudes = Solicitud.objects.filter(arrendatario=perfil)

    return render(
        request,
        'dashboard.html',
        {
            'perfil': perfil,
            'user_type': user_type,
            'inmuebles': inmuebles,
            'solicitudes': solicitudes
        }
    )




@login_required
def update_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, propietario__user=request.user)

    if request.method == 'POST':
        # Process form submission to update Inmueble
        inmueble.nombre_inmueble = request.POST.get('nombre_inmueble')
        inmueble.descripcion = request.POST.get('descripcion')
        inmueble.m2_construido = request.POST.get('m2_construido')
        inmueble.numero_banos = request.POST.get('numero_banos')
        inmueble.numero_hab = request.POST.get('numero_hab')
        inmueble.direccion = request.POST.get('direccion')
        inmueble.numero_estacionam = request.POST.get('numero_estacionam')
        inmueble.precio = request.POST.get('precio')
        inmueble.save()
        messages.success(request, "Inmueble updated successfully.")
        return redirect('dashboard')

    return render(request, 'update_inmueble.html', {'inmueble': inmueble})


@login_required
def delete_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id, propietario__user=request.user)
    inmueble.delete()
    messages.success(request, "Inmueble deleted successfully.")
    return redirect('dashboard')


@login_required
def cancel_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, arrendatario__user=request.user)
    solicitud.delete()
    messages.success(request, "Solicitud cancelled successfully.")
    return redirect('dashboard')



def about(request):
   return render(request, 'about.html')

def exito(request):
   return render(request, 'exito.html')

def exito_reg(request):
   return render(request, 'exito_reg.html')

def sign_up(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():            
            user = form.save()
            
            perfil = PerfilUsuario.objects.create(
                user=user,
                tipo_usuario=form.cleaned_data['tipo_usuario'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                rut=form.cleaned_data['rut'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                correo=form.cleaned_data['correo'] 
            )
            
            login(request, user)
            return redirect('/exito_reg/')  
        else:
            print(form.errors)  
            messages.error(request, "Error en el formulario. Verifica los datos.")
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def log_in(request):
    if request.method == 'POST': 
        form = AuthenticationForm(data=request.POST)  
        if form.is_valid():            
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:  
                login(request, user)  
                return redirect('homepage')  
        else:            
            messages.error(request, 'Usuario o contraseña incorrectos.')

    else:       
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('homepage')


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PerfilUsuarioForm
from .models import PerfilUsuario
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request):
    perfil = PerfilUsuario.objects.get(user=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil)  # Pass instance to pre-fill data
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('dashboard')  # Redirect after successful update
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PerfilUsuarioForm(instance=perfil)  # Pre-fill form with existing data

    return render(request, 'update_profile.html', {'form': form})


@login_required
def delete_profile(request):
    perfil = PerfilUsuario.objects.get(user=request.user)
    user = perfil.user
    user.delete()
    messages.success(request, "Perfil eliminado exitosamente.")
    return redirect('homepage')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateInmuebleForm
from .models import PerfilUsuario

@login_required
def create_inmueble(request):
    if request.method == 'POST':
        form = CreateInmuebleForm(request.POST, request.FILES)  # Add request.FILES to handle image upload
        if form.is_valid():
            inmueble = form.save(commit=False)
            propietario = PerfilUsuario.objects.get(user=request.user)
            if propietario.tipo_usuario.tipo_usuario != 'arrendador':
                messages.error(request, "Solo los arrendadores pueden crear inmuebles.")
                return redirect('dashboard')
            inmueble.propietario = propietario
            inmueble.save()
            messages.success(request, "Inmueble creado con éxito.")
            return redirect('dashboard')
    else:
        form = CreateInmuebleForm()
    return render(request, 'create_inmueble.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Inmueble
from .forms import UpdateInmuebleForm

def update_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)

    if request.method == 'POST':
        form = UpdateInmuebleForm(request.POST, request.FILES, instance=inmueble)  # Ensure FILES is passed
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Redirect to the detail page after save
    else:
        form = UpdateInmuebleForm(instance=inmueble)

    return render(request, 'update_inmueble.html', {'form': form, 'inmueble': inmueble})



from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def apply_for_solicitud(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    perfil = PerfilUsuario.objects.get(user=request.user)

    if perfil.tipo_usuario.tipo_usuario != 'arrendatario':  # Only tenants can apply
        return HttpResponseForbidden("Only tenants can apply for a property.")

    # Check if a solicitud already exists for this inmueble and tenant
    existing_solicitud = Solicitud.objects.filter(arrendatario=perfil, inmueble=inmueble).exists()
    if existing_solicitud:
        messages.error(request, "You have already applied for this property.")
        return redirect('homepage')

    # Create a new solicitud
    Solicitud.objects.create(arrendatario=perfil, inmueble=inmueble)
    messages.success(request, "Your request to rent this property has been sent.")
    
    # Redirect to the confirmation template
    return render(request, 'peticion_enviada.html')  # This is where the success message will be shown


@login_required
def manage_solicitud(request, solicitud_id, action):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id, inmueble__propietario__user=request.user)
    if action == 'approve':
        solicitud.estado = 'aprobada'
        messages.success(request, f"Solicitud for {solicitud.inmueble} approved.")
    elif action == 'reject':
        solicitud.estado = 'rechazada'
        messages.error(request, f"Solicitud for {solicitud.inmueble} rejected.")
    solicitud.save()
    return redirect('dashboard')


from django.shortcuts import render

def acerca(request):
    return render(request, 'acerca.html')

def contacto(request):
    return render(request, 'contacto.html')
