from django.urls import path,include
from .views import ProductoListAPIView, ProductoDeleteAPIView, ProductoListView, ProductoDeleteView, DemoView

urlpatterns = [
    path('api/productos/', ProductoListAPIView.as_view(), name='produto-list-api'),
    path('api/productos/<int:pk>/delete', ProductoDeleteAPIView.as_view(), name='producto-delete-api'),

    #HTML Frontend
    path('productos/',ProductoListView.as_view(), name='producto-list-html'),
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='producto-delete-html'),
    path('demo/', DemoView.as_view(), name='demo'),
    path('',ProductoListView.as_view(), name='home'),
]
