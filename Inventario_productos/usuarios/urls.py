from django.urls import path,include
from .views import UsuarioListAPIView,UsuarioDetailAPIView, UsuarioDeleteAPIView, UsuarioListView, UsuarioDeleteView, DemoView, UsuarioAjaxView

urlpatterns = [
    #API Endpoints
    path('api/usuarios/', UsuarioListAPIView.as_view(), name='usuario-list-api'),
    path('api/usuarios/<int:pk>/', UsuarioDetailAPIView.as_view(), name='usuario-detail-api'),
    path('api/usuarios/<int:pk>/delete', UsuarioDeleteAPIView.as_view(), name='usuario-delete-api'),

    #AJAX Endpoints para el frontend
    path('ajax/usuarios/', UsuarioAjaxView.as_view(), name='usuario-ajax'),
    path('ajax/usuarios/<int:pk>/', UsuarioAjaxView.as_view(), name='usuario-ajax-detail'),

    #HTML Frontend
    path('usuarios/',UsuarioListView.as_view(), name='usuario-list-html'),
    path('usuarios/<int:pk>/delete/', UsuarioDeleteView.as_view(), name='usuario-delete-html'),
    path('demo/', DemoView.as_view(), name='demo'),
    path('',UsuarioListView.as_view(), name='home'),
]
