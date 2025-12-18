from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    # Guardamos la ruta de la imagen como texto para facilitar el uso de static files
    imagen_url = models.CharField(max_length=200, help_text="Ej: img/reservas/evento1.jpg")
    capacidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return self.titulo

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='confirmada')

    class Meta:
        # Un usuario solo puede reservar una vez el mismo evento
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.titulo}"