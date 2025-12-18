from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Evento, Reserva
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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
            messages.success(request, f'¡Bienvenido {username}! Tu cuenta ha sido creada. Por favor inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def perfil(request):
    """Muestra las reservas del usuario"""
    mis_reservas = Reserva.objects.filter(usuario=request.user).select_related('evento').order_by('-fecha_reserva')
    return render(request, 'perfil.html', {'reservas': mis_reservas})

# --- VISTAS DE RESERVAS ---

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('fecha_inicio')
    return render(request, 'reservar.html', {'eventos': eventos})

@login_required
def reservar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Validar si ya tiene reserva
    if Reserva.objects.filter(usuario=request.user, evento=evento).exists():
        messages.warning(request, f'Ya tienes una reserva para {evento.titulo}.')
        return redirect('perfil')
    
    # Validar capacidad
    if evento.reservas.count() >= evento.capacidad:
        messages.error(request, 'Lo sentimos, no quedan cupos disponibles.')
        return redirect('lista_eventos')

    # Crear reserva
    Reserva.objects.create(usuario=request.user, evento=evento)
    messages.success(request, f'¡Reserva confirmada para {evento.titulo}!')
    
    # Redirigir al perfil para ver el ticket
    return redirect('perfil')
