from django.contrib import admin
from .models import Evento, Reserva

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'lugar', 'capacidad', 'precio')
    search_fields = ('titulo', 'lugar')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_reserva', 'estado')
    list_filter = ('evento', 'fecha_reserva')