from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    proveedor = models.CharField(max_length=100, blank=True)
    porcentaje_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
