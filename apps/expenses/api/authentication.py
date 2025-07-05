"""
Autenticación personalizada para la API REST usando Bearer Token

Este módulo contiene la autenticación personalizada que reutiliza el mismo
sistema de tokens que ya usas para los webhooks con n8n.
"""

from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings


class BearerTokenAuthentication(authentication.BaseAuthentication):
    """
    Autenticación personalizada usando Bearer Token para la API REST
    
    Usa un token específico para la API (separado del webhook):
    - Desarrollo: 'dev-api-token-123' 
    - Producción: Token seguro desde .env.production (N8N_API_TOKEN)
    
    Esto proporciona mejor seguridad al separar tokens por propósito:
    - N8N_WEBHOOK_TOKEN → Solo para webhooks (presupuesto 90%)
    - N8N_API_TOKEN → Solo para API REST (reportes)
    """
    
    def authenticate(self, request):
        """
        Autentica el request usando el Bearer Token del header Authorization
        
        Args:
            request: HTTP request de Django
            
        Returns:
            tuple: (user, token) si la autenticación es exitosa
            None: si no hay token o el header no es válido
            
        Raises:
            AuthenticationFailed: si el token es inválido
        """
        
        # Obtener header Authorization
        auth_header = authentication.get_authorization_header(request).split()
        
        # Verificar que el header existe y tiene el formato correcto
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None
            
        if len(auth_header) == 1:
            msg = 'Token Bearer inválido. No se proporcionó token.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Token Bearer inválido. El token no debe contener espacios.'
            raise exceptions.AuthenticationFailed(msg)
            
        # Extraer el token
        token = auth_header[1].decode('utf-8')
        
        # Verificar que el token coincide con el configurado para la API
        expected_token = getattr(settings, 'N8N_API_TOKEN', 'dev-api-token-123')
        
        if token != expected_token:
            raise exceptions.AuthenticationFailed('Token Bearer inválido.')
            
        # Retornar None como usuario ya que usamos AllowAny
        # Solo necesitamos validar el token, no un usuario específico
        return (None, token)
    
    def authenticate_header(self, request):
        """
        Retorna el header WWW-Authenticate para responses 401
        """
        return 'Bearer' 