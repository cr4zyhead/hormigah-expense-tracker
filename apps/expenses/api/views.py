"""
Vistas para la API REST

Este módulo contiene las vistas que manejan los endpoints de la API
para que n8n pueda obtener los datos necesarios para los reportes.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.utils import timezone
from datetime import timedelta
from apps.expenses.models import Expense, Budget
from .serializers import UserActiveSerializer, UserCompleteSerializer
from .authentication import BearerTokenAuthentication


class ActiveUsersView(generics.ListAPIView):
    """
    Vista para obtener la lista de usuarios activos
    
    Endpoint: GET /api/users/active/
    
    Criterios para "usuario activo":
    - Tiene presupuesto configurado (Budget existe)
    - Tiene alertas por email activadas (email_alerts_enabled=True)
    - Ha registrado gastos en los últimos 30 días
    
    Respuesta:
    [
        {
            "id": 1,
            "username": "juan",
            "email": "juan@email.com"
        },
        ...
    ]
    """
    
    serializer_class = UserActiveSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Retorna los usuarios que cumplen los criterios de "activo"
        
        Returns:
            QuerySet: Usuarios activos filtrados
        """
        
        # Fecha límite para considerar gastos recientes (últimos 30 días)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        
        # Filtrar usuarios que:
        # 1. Tienen presupuesto configurado
        # 2. Tienen alertas por email activadas
        # 3. Han registrado gastos en los últimos 30 días
        active_users = User.objects.filter(
            # Tiene presupuesto configurado
            budget__isnull=False,
            # Tiene alertas por email activadas
            budget__email_alerts_enabled=True,
            # Ha registrado gastos en los últimos 30 días
            expenses__date__gte=thirty_days_ago
        ).distinct().order_by('username')
        
        return active_users
    
    def list(self, request, *args, **kwargs):
        """
        Maneja la petición GET y retorna la lista de usuarios activos
        
        Args:
            request: HTTP request
            
        Returns:
            Response: Lista de usuarios activos en formato JSON
        """
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Agregar información adicional útil para n8n
        response_data = {
            'users': serializer.data,
            'total_active_users': queryset.count(),
            'timestamp': timezone.now().isoformat(),
            'criteria': {
                'has_budget': True,
                'email_alerts_enabled': True,
                'recent_expenses_days': 30
            }
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class UserCompleteView(generics.RetrieveAPIView):
    """
    Vista para obtener los datos completos de un usuario específico
    
    Endpoint: GET /api/users/{user_id}/complete/
    
    Incluye:
    - Datos del usuario
    - Presupuesto configurado
    - Historial completo de gastos
    - Resúmenes mensuales
    - Resúmenes por categorías
    
    Respuesta:
    {
        "user": { ... },
        "budget": { ... },
        "complete_history": {
            "all_expenses": [ ... ],
            "monthly_summaries": { ... },
            "categories_summary": { ... }
        }
    }
    """
    
    serializer_class = UserCompleteSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        """
        Retorna los usuarios que tienen datos para mostrar
        
        Returns:
            QuerySet: Usuarios con presupuesto configurado
        """
        
        # Solo retornar usuarios que tienen presupuesto configurado
        # (no tiene sentido generar reportes sin presupuesto)
        return User.objects.filter(
            budget__isnull=False
        ).select_related('budget')
    
    def retrieve(self, request, *args, **kwargs):
        """
        Maneja la petición GET y retorna los datos completos del usuario
        
        Args:
            request: HTTP request
            
        Returns:
            Response: Datos completos del usuario en formato JSON
        """
        
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            # Agregar metadata útil para n8n
            response_data = {
                **serializer.data,
                'metadata': {
                    'generated_at': timezone.now().isoformat(),
                    'api_version': '1.0',
                    'data_complete': True
                }
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {
                    'error': 'Usuario no encontrado o no tiene presupuesto configurado',
                    'detail': 'El usuario debe tener un presupuesto configurado para generar reportes'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Error interno del servidor',
                    'detail': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 