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
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# --- VISTAS DE RESERVAS ---

def lista_eventos(request):
    """Muestra todos los eventos disponibles ordenados por fecha"""
    eventos = Evento.objects.all().order_by('fecha_inicio')
    return render(request, 'reservar.html', {'eventos': eventos})

@login_required(login_url='/login/')
def reservar_evento(request, evento_id):
    """Procesa la reserva. Solo usuarios logueados pueden entrar aquí."""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # 1. Validar si ya reservó antes
    reserva_existente = Reserva.objects.filter(usuario=request.user, evento=evento).exists()
    
    if reserva_existente:
        messages.warning(request, f'Ya tienes una reserva registrada para {evento.titulo}.')
    
    # 2. Validar capacidad
    elif evento.reservas.count() >= evento.capacidad:
        messages.error(request, 'Lo sentimos, no quedan cupos disponibles.')
        
    else:
        # 3. Crear la reserva
        Reserva.objects.create(usuario=request.user, evento=evento)
        messages.success(request, f'¡Reserva exitosa para {evento.titulo}! Te esperamos.')
    
    return redirect('lista_eventos')
