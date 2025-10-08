from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'costo', 'proveedor', 'porcentaje_ganancia', 'cantidad', 'creado')
    search_fields = ('nombre', 'proveedor')
    list_filter = ('creado', 'proveedor')
