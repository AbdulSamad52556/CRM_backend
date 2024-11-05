# urls.py
from django.urls import path
from .views import PropertyCreateView,PropertyViewSet, UnitCreateView, UnitListView, PropertyListView

urlpatterns = [
    path('properties/', PropertyCreateView.as_view(), name='property-create'),
    path('get-properties/', PropertyViewSet.as_view({'get': 'list'}), name='property-get'),
    path('units/create/', UnitCreateView.as_view(), name='unit-create'),
    path('units/', UnitListView.as_view(), name='units'),
    path('all-properties/', PropertyListView.as_view(), name='property-list'),
]
