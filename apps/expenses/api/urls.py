"""
URLs para la API REST

Este módulo define las rutas de la API que n8n utilizará para
obtener los datos de usuarios y generar reportes.
"""

from django.urls import path
from .views import ActiveUsersView, UserCompleteView

# Namespace para la API
app_name = 'expenses_api'

urlpatterns = [
    # Endpoint para obtener lista de usuarios activos
    # GET /api/users/active/
    path(
        'users/active/',
        ActiveUsersView.as_view(),
        name='active-users'
    ),
    
    # Endpoint para obtener datos completos de un usuario
    # GET /api/users/{user_id}/complete/
    path(
        'users/<int:id>/complete/',
        UserCompleteView.as_view(),
        name='user-complete'
    ),
] 