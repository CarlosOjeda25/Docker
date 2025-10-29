from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Producto
from .serializers import ProductoSerializer
from rest_framework import generics


# Listar Productos
class ProductoListAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({
                'error': 'Datos Invalidos.',
                'details': serializer.errors
            },status=400)
        try:
            self.perform_create(serializer)
            return JsonResponse(serializer.data, status=200)
        except Exception as e:
            return JsonResponse({
                    'error': 'Error interno del servidor.',
                    'details': str(e)
            }, status=500)


#Detalle Producto
class ProductoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def retrive(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data, status=200)
        except Exception as e:
            return JsonResponse({
                'error': 'Producto no encontrado.',
                'details': str(e)
            }, status=404)
    
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if not serializer.is_valid():
                return JsonResponse({
                    'error': 'Datos Invalidos.',
                    'details': serializer.errors
                },status=400)
            self.perform_update(serializer)
            return JsonResponse(serializer.data, status=200)
        except Producto.DoesNotExist as e:
            return JsonResponse({'error': 'Producto no encontrado.', 'details': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor.', 'details': str(e)}, status=500)
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return JsonResponse({'message': 'Producto eliminado exitosamente.'}, status=200)
        except Producto.DoesNotExist as e:
            return JsonResponse({'error': 'Producto no encontrado.', 'details': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor.', 'details': str(e)}, status=500)


#Eliminar Producto
class ProductoDeleteAPIView(generics.DestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


#Html views para frontend
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'
    ordering = ['-creado']
    
class DemoView(ListView):
    model = Producto
    template_name = 'productos/demo.html'
    context_object_name = 'productos'


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto-list-html')
    context_object_name = 'producto'

    def form_valid(self, form):
        producto = self.get_object()
        print("----------------------------------------------------")
        print(f'Delete request received - Eliminando producto: {producto.nombre} (ID: {producto.id})')
        messages.success(self.request, f'El Producto "{producto.nombre}" eliminado exitosamente.')
        return super().form_valid(form)
    
# vista para manejar ajax

@method_decorator(csrf_exempt, name='dispatch')
class ProductoAjaxView(generics.GenericAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def post(self, request, *args, **kwargs):
        """Crear nuevo producto via AJAX"""
        print("*************************************************")
        print("POST request received - Creando nuevo producto")
        print(request.body)
        try:
            data ={
                'nombre': request.POST.get('nombre'),
                'descripcion': request.POST.get('descripcion',''),
                'precio': request.POST.get('precio'),
                'cantidad': request.POST.get('cantidad',1),
                'costo': request.POST.get('costo', 0.00),
                'proveedor': request.POST.get('proveedor', ''),
                'porcentaje_ganancia': request.POST.get('porcentaje_ganancia', 0.00)
            }

            producto =  Producto.objects.create(**data)
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'cantidad': producto.cantidad,
                'costo': str(producto.costo),
                'proveedor': producto.proveedor,
                'porcentaje_ganancia': str(producto.porcentaje_ganancia),
                'creado': producto.creado.strftime('%d/%m/%Y %H:%M')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

    def put(self, request, pk, *args, **kwargs):
        """actualizar producto via AJAX"""

        try:
            producto = get_object_or_404(Producto, pk=pk)

            data = json.loads(request.body)

            # Filtrar datos no necesarios para la actualización
            update_data = {k: v for k, v in data.items() if k not in ['id', 'csrfmiddlewaretoken']}

            serializer = ProductoSerializer(producto, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': str(producto.precio),
                    'cantidad': producto.cantidad,
                    'costo': str(producto.costo),
                    'proveedor': producto.proveedor,
                    'porcentaje_ganancia': str(producto.porcentaje_ganancia),
                    'creado': producto.creado.strftime('%d/%m/%Y %H:%M')
                })
            else:
                return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)