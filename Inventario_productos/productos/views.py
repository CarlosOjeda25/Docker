from django.shortcuts import render
from.models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics

# Listar Productos
class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

#Eliminar Producto
class ProductoDeleteView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
