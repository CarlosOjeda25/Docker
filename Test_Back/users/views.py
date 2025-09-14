from django.shortcuts import render
from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSelializer
from .models import Profile


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions() 
    
    @action(detail=False, methods=['GET']) 
    def me(self, request):
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
    
    @action(detail=False, methods=['GET','PUT'])
    def profile(self,request, pk=None):
        user = self.get_object()
        if request.method == 'GET':
            serializer = ProfileSelializer(user.profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ProfileSelializer(user.profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)