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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, decorators


# Listar Usuarios
class UsuarioListAPIView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

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

#Detalle Usuario
class UsuarioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data, status=200)
        except Exception as e:
            return JsonResponse({
                'error': 'Usuario no encontrado.',
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
        except Usuario.DoesNotExist as e:
            return JsonResponse({'error': 'Usuario no encontrado.', 'details': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor.', 'details': str(e)}, status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return JsonResponse({'message': 'Usuario eliminado exitosamente.'}, status=200)
        except Usuario.DoesNotExist as e:
            return JsonResponse({'error': 'Usuario no encontrado.', 'details': str(e)}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Error interno del servidor.', 'details': str(e)}, status=500)


    def post(self, request, *args, **kwargs):
        usuario = self.get_object()
        letra = str(request.data.get('letra'))

        if not usuario.palabra_clave or getattr(usuario, 'estado_juego', 'jugando') == 'completado':
            return Response({
                'mensaje': 'El juego ya ha sido completado. No puedes enviar más letras.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not letra or len(letra) != 1:
            return Response({'error': 'Debe enviar una letra única.'}, status=status.HTTP_400_BAD_REQUEST)

        palabra = usuario.palabra_clave.lower()
        letra = letra.lower()

        if letra in palabra:
            nueva = palabra.replace(letra, '')
            usuario.palabra_clave = nueva

            if not nueva:
                usuario.estado_juego = 'completado' 
                usuario.save()
                return Response({
                    'mensaje': '¡Felicidades! Has adivinado toda la palabra.',
                    'estado': 'completado'
                }, status=status.HTTP_200_OK)

            usuario.save()
            return Response({
                'mensaje': f'Letra "{letra}" encontrada.',
                'restante': usuario.palabra_clave
            }, status=status.HTTP_200_OK)

        return Response({
            'error': f'La letra "{letra}" no está en la palabra.'
        }, status=status.HTTP_400_BAD_REQUEST)

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



