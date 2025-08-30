from django.urls import path
from . import views  # Import views from the events app

urlpatterns = [
    path('', views.home, name='home'),  # Root URL maps to home view
]
