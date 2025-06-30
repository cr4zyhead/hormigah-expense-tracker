#!/usr/bin/env python
"""
Script de prueba para enviar webhook de alerta de presupuesto a n8n

Simula el webhook que Django envía cuando un usuario supera el 90% del presupuesto.
Uso: docker-compose exec web python test_webhooks.py
"""

import os
import sys
import django
import requests
from datetime import datetime

# Configurar Django
# Ir 3 niveles arriba desde apps/expenses/tests/ hasta la raíz del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.conf import settings

def test_budget_webhook():
    """
    Envía un webhook de prueba a n8n para testing
    
    Esta función simula exactamente lo que Django hace cuando:
    1. Un usuario agrega un gasto
    2. Django calcula que superó el 90% del presupuesto
    3. Django llama a send_webhook_to_n8n() desde util_crud_operations.py
    """
    
    # URL del webhook de n8n (TEST URL para "Listen for test event")
    # IMPORTANTE: Desde Docker usar 'n8n:5678', desde host usar 'localhost:5678'
    # Para testing usar: http://n8n:5678/webhook-test/budget-alert
    webhook_url = "http://n8n:5678/webhook-test/budget-alert"
    
    # Payload de prueba simulando alerta del 90%
    # Estos son los MISMOS datos que Django envía en la función real
    payload = {
        'user_id': 1,                                        # ID del usuario en Django
        'user_name': 'Usuario Prueba',                       # Nombre completo o username
        'user_email': 'joseolmostech@gmail.com',            # Email para enviar alerta
        'budget_limit': 500.00,                              # Límite mensual configurado
        'current_spending': 465.50,                          # Gastos actuales del mes
        'percentage': 93.1,                                  # Porcentaje calculado (465.5/500*100)
        'alert_type': 'budget_90_percent',                   # Tipo de alerta
        'message': 'Has alcanzado el 93.1% de tu presupuesto mensual',  # Mensaje personalizado
        'timestamp': datetime.now().isoformat()             # Timestamp de la alerta
    }
    
    # Headers con Bearer Token - DEBE coincidir con la configuración de n8n
    # En desarrollo usa 'dev-token-123' (fallback en settings/local.py)
    # En producción usa el token seguro de .env.production
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer dev-token-123'  # Token configurado en n8n
    }
    
    try:
        print("[INFO] Enviando webhook de prueba a n8n...")
        print(f"[URL] {webhook_url}")
        print(f"[TOKEN] dev-token-123")
        print(f"[PAYLOAD] {payload}")
        
        response = requests.post(
            webhook_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        
        print(f"\n[RESPONSE] Respuesta recibida:")
        print(f"[STATUS] {response.status_code}")
        print(f"[BODY] {response.text}")
        
        if response.status_code == 200:
            print("\n[SUCCESS] Webhook enviado exitosamente!")
        else:
            print(f"\n[WARNING] Error en webhook: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Error enviando webhook: {e}")

if __name__ == '__main__':
    test_budget_webhook()

"""
INTERPRETACION DE RESULTADOS DEL TEST

RESULTADOS EXITOSOS:
[SUCCESS] Webhook enviado exitosamente!
- Status 200: n8n recibio y proceso el webhook
- En n8n veras los datos JSON en la seccion OUTPUT del Webhook node

ERRORES COMUNES:

1. [ERROR] Connection refused
   - Problema: n8n no esta corriendo
   - Solucion: docker-compose up -d

2. [WARNING] Error en webhook: 404
   - Problema: Endpoint no existe en n8n
   - Solucion: Verificar que el workflow este GUARDADO y ACTIVO
   - O usar "Listen for test event" si estas probando

3. [WARNING] Error en webhook: 401/403
   - Problema: Error de autenticacion
   - Solucion: Verificar Bearer Token en n8n (Authorization: Bearer dev-token-123)

VERIFICACION EN N8N:
1. Acceder a http://localhost:5678
2. Abrir el workflow "Budget Alert Emails"
3. Click en el Webhook node
4. En la seccion OUTPUT deberias ver:
   {
     "user_id": 1,
     "user_name": "Usuario Prueba",
     "user_email": "test@example.com",
     "budget_limit": 500.0,
     "current_spending": 465.5,
     "percentage": 93.1,
     "alert_type": "budget_90_percent",
     "message": "Has alcanzado el 93.1% de tu presupuesto mensual",
     "timestamp": "2025-06-29T..."
   }


DATOS SIMULADOS:
Este test simula un usuario que:
- Tiene presupuesto de 500 euros
- Ha gastado 465.50 euros (93.1%)
- Supero el umbral del 90%
- Deberia recibir alerta por email

FLUJO REAL EN PRODUCCION:
1. Usuario agrega gasto real en Django
2. Django calcula: gasto_actual / presupuesto * 100
3. Si >= 90%: Django llama send_webhook_to_n8n()
4. n8n recibe webhook y envia email al usuario
5. Usuario recibe alerta: "Has superado el 90% de tu presupuesto"
""" 