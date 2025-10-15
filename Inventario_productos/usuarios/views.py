from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework import generics


# Listar Usuarios
class UsuarioListAPIView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

#Eliminar Usuario
class UsuarioDeleteAPIView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


#Html views para frontend
class UsuarioListView(ListView):
    model = Usuario
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    ordering = ['-fecha_creacion']
    
class DemoView(ListView):
    model = Usuario
    template_name = 'usuarios/demo.html'
    context_object_name = 'usuarios'


class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario-list-html')
    context_object_name = 'usuario'

    def form_valid(self, form):
        usuario = self.get_object()
        print("----------------------------------------------------")
        print(f'Delete request received - Eliminando Usuario: {usuario.nombre} (ID: {usuario.id})')
        messages.success(self.request, f'El Usuario "{usuario.nombre}" eliminado exitosamente.')
        return super().form_valid(form)
    
# vista para manejar ajax

@method_decorator(csrf_exempt, name='dispatch')
class UsuarioAjaxView(generics.GenericAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        """Crear nuevo Usuario via AJAX"""
        print("*************************************************")
        print("POST request received - Creando nuevo Usuario")
        print(request.body)
        try:
            data ={
                'nombre': request.POST.get('nombre'),
                'apellido': request.POST.get('apellido',''),
                'edad': request.POST.get('edad'),
                'email': request.POST.get('email'),
                'telefono': request.POST.get('telefono', ''),
                'direccion': request.POST.get('direccion', '')
            }

            usuario =  Usuario.objects.create(**data)
            return JsonResponse({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'edad': usuario.edad,
                'email': usuario.email,
                'telefono': usuario.telefono,
                'direccion': usuario.direccion,
                'fecha_creacion': usuario.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        

    def put(self, request, pk, *args, **kwargs):
        """actualizar Usuario via AJAX"""

        try:
            usuario = get_object_or_404(Usuario, pk=pk)

            data = json.loads(request.body)

            # Filtrar datos no necesarios para la actualización
            update_data = {k: v for k, v in data.items() if k not in ['id', 'csrfmiddlewaretoken']}

            serializer = UsuarioSerializer(usuario, data=update_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'edad': usuario.edad,
                    'email': usuario.email,
                    'telefono': usuario.telefono,
                    'direccion': usuario.direccion,
                    'fecha_creacion': usuario.fecha_creacion.strftime('%d/%m/%Y %H:%M')
                })
            else:
                return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
