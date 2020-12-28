from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('bus_create',views.bus_create, name="bus_create"),
    path('bus_update/<str:pk>',views.bus_update, name="bus_update"),
    path('bus_delete/<str:pk>',views.bus_delete, name="bus_delete"),
]