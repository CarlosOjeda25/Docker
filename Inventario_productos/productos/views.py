from django.shortcuts import render, get_list_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from json import JsonResponse

from.models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics


# Listar Productos
class ProductoListAPIView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

#Eliminar Producto
class ProductoDeleteAPIView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


#Html views para frontend
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list-html'
    context_object_name = 'productos'
    ordeingring = ['-creado']
    
class DemoView(ListView):
    model = Producto
    template_name = 'productos/demo.html'
    context_object_name = 'productos'


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete-html'
    success_url = reverse_lazy('producto-list.html')
    context_object_name = 'producto'

    def delete(self, request, *args, **kwargs):
        producto = self.get_object()
        messages.success(request, f'El Producto "{producto.nombre}" eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
    
# vista para manejar ajax

@method_decorator(csrf_exempt, name='dispatch')
class ProductoAjaxView(generics.GenericAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def post(self, request, *args, **kwargs):
        """Crear nuevo producto via AJAX"""
        
        try:
            data ={
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion',''),
                'precio': request.POST.get('precio'),
            }

            producto =  property.objects.create(**data)
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'creado': producto.creado.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

    def put(self, request, *args, **kwargs):
        """Crear nuevo producto via AJAX"""
        
        try:
            data ={
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion',''),
                'precio': request.POST.get('precio'),
            }

            producto =  property.objects.create(**data)
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'creado': producto.creado.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)