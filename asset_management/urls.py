# urls.py
from django.urls import path
from .views import PropertyCreateView,PropertyViewSet

urlpatterns = [
    path('properties/', PropertyCreateView.as_view(), name='property-create'),
    path('get-properties/', PropertyViewSet.as_view({'get': 'list'}), name='property-get'),
]
