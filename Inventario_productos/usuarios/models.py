from django.db import models
import random

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    palabra_clave = models.CharField(max_length=50, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_juego = models.CharField(
    max_length=20,
    default='jugando',
    choices=[('jugando', 'Jugando'), ('completado', 'Completado')]
)


    PROFESIONES = [
        'Medico', 'Ingeniero', 'Profesor', 'Abogado', 'Arquitecto', 'Contador', 'Enfermero', 'Dentista',
        'Programador', 'Disenador', 'Chef', 'Periodista', 'Policia', 'Bombero', 'Piloto', 'Mecanico',
        'Electricista', 'Plomero', 'Carpintero', 'Pintor', 'Fotografo', 'Actor', 'Musico', 'Escritor',
        'Cientifico', 'Investigador', 'Veterinario', 'Psicologo', 'Terapeuta', 'Entrenador', 'Deportista',
        'Empresario', 'Gerente', 'Secretario', 'Recepcionista', 'Vendedor', 'Cajero', 'Cocinero',
        'Camarero', 'Chofer', 'Taxista', 'Guardia de Seguridad', 'Limpieza', 'Jardinero', 'Peluquero',
        'Estilista', 'Maquillador', 'Modelo', 'Influencer', 'Streamer', 'YouTuber', 'Blogger'
    ]

    def save(self, *args, **kwargs):
        if not self.palabra_clave:
            self.palabra_clave = random.choice(self.PROFESIONES)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
