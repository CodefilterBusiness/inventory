from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_master, name='home'),  # Maps root URL to the home view
]
