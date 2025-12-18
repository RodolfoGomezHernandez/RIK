from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Evento, Reserva
from django.contrib.auth.decorators import login_required

def home(request):
    # Solo una línea return. La anterior estaba bloqueando.
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})



# --- VISTAS GENERALES ---

def home(request):
    return render(request, 'home.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # Mensaje de éxito claro
            messages.success(request, f'¡Bienvenido {username}! Tu cuenta ha sido creada exitosamente. Por favor inicia sesión.')
            # Redirigir al login para que ingrese con sus nuevas credenciales
            return redirect('login')
        else:
            # Si hay error, el formulario lo mostrará, pero añadimos un mensaje general
            messages.error(request, 'Hubo un error en el registro. Por favor verifica los datos.')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def perfil(request):
    """Muestra el panel del usuario con sus reservas"""
    # Obtenemos las reservas del usuario actual, ordenadas por fecha más reciente
    mis_reservas = Reserva.objects.filter(usuario=request.user).select_related('evento').order_by('-fecha_reserva')
    return render(request, 'perfil.html', {'reservas': mis_reservas})

# --- VISTAS DE RESERVAS ---

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('fecha_inicio')
    return render(request, 'reservar.html', {'eventos': eventos})

@login_required(login_url='/login/')
def reservar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    reserva_existente = Reserva.objects.filter(usuario=request.user, evento=evento).exists()
    
    if reserva_existente:
        messages.warning(request, f'Ya tienes una reserva registrada para {evento.titulo}.')
    elif evento.reservas.count() >= evento.capacidad:
        messages.error(request, 'Lo sentimos, no quedan cupos disponibles.')
    else:
        Reserva.objects.create(usuario=request.user, evento=evento)
        # Mensaje de éxito y redirección al perfil para ver la reserva
        messages.success(request, f'¡Reserva confirmada para {evento.titulo}!')
        return redirect('perfil') # <--- CAMBIO: Redirige al perfil en lugar de la lista
    
    return redirect('lista_eventos')
