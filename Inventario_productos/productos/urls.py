from django.urls import path,include
from .views import ProductoListView, ProductoDeleteView

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/<int:pk>/delete', ProductoDeleteView.as_view(), name='producto-delete'),
]
