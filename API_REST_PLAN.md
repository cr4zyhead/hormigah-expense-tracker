# 📋 API REST para Gastos Hormiga - Plan de Implementación

## 🎯 **OBJETIVO**
Crear una API REST básica con Django REST Framework (DRF) que permita a n8n obtener datos de usuarios para generar reportes mensuales automáticos con IA.

---

## 🔐 **SISTEMA DE AUTENTICACIÓN**

### **Bearer Token (Mismo estilo que webhooks, pero token separado)**
- ✅ **Desarrollo:** `dev-api-token-123` (configurado en `config/settings/local.py`)
- ✅ **Producción:** Token seguro en `.env.production` (variable `N8N_API_TOKEN`)

### **Headers requeridos:**
```http
Authorization: Bearer dev-api-token-123
Content-Type: application/json
```

### **Configuración de tokens separados:**
- **Webhooks:** `N8N_WEBHOOK_TOKEN = 'dev-token-123'` (alertas presupuesto 90%)
- **API REST:** `N8N_API_TOKEN = 'dev-api-token-123'` (reportes mensuales)

### **Ventajas de tokens separados:**
- 🔒 **Mayor seguridad** (revocar independientemente)
- 🎯 **Responsabilidades claras** (webhook vs API)
- 📊 **Mejor auditoría** (logs separados por propósito)

---

## 🚀 **ENDPOINTS A IMPLEMENTAR**

### **1. Lista de usuarios activos**
```http
GET /api/users/active/
```

**Criterios para "usuario activo":**
- Tiene presupuesto configurado (`Budget` existe)
- Tiene alertas por email activadas (`email_alerts_enabled=True`) 
- Ha registrado gastos en los últimos 30 días

**Respuesta:**
```json
[
  {
    "id": 1,
    "username": "juan",
    "email": "juan@email.com"
  },
  {
    "id": 2,
    
    "username": "maria", 
    "email": "maria@email.com"
  }
]
```

### **2. Datos completos del usuario**
```http
GET /api/users/{user_id}/complete/
```

**Respuesta completa con todo el historial:**
```json
{
  "user": {
    "id": 1,
    "username": "juan",
    "email": "juan@email.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "date_joined": "2023-03-15T10:30:00Z"
  },
  "budget": {
    "monthly_limit": 500.00,
    "warning_percentage": 75,
    "critical_percentage": 90,
    "email_alerts_enabled": true,
    "created_at": "2023-03-15T10:30:00Z"
  },
  "complete_history": {
    "first_expense": "2023-03-15",
    "last_expense": "2024-01-28", 
    "total_months_active": 11,
    "total_expenses": 4520.75,
    "total_expense_count": 245,
    "all_expenses": [
      {
        "id": 1,
        "amount": 25.50,
        "description": "Café Starbucks",
        "date": "2024-01-28",
        "location": "Centro Comercial",
        "category": {
          "id": 1,
          "name": "Café",
          "icon": "☕",
          "color": "#8B4513"
        },
        "created_at": "2024-01-28T09:30:00Z"
      }
      // ... todos los gastos históricos
    ],
    "monthly_summaries": {
      "2023-03": {
        "total": 120.00,
        "count": 8,
        "categories": {
          "Café": 60.00,
          "Delivery": 60.00
        }
      },
      "2023-04": {
        "total": 340.00,
        "count": 15,
        "categories": {
          "Café": 180.00,
          "Delivery": 120.00,
          "Transporte": 40.00
        }
      }
      // ... todos los meses
    },
    "categories_summary": {
      "Café": {
        "total": 1250.00,
        "count": 85,
        "percentage": 27.6
      },
      "Delivery": {
        "total": 2100.00,
        "count": 95,
        "percentage": 46.5
      }
      // ... todas las categorías
    }
  }
}
```

---

## ⚙️ **FLUJO DE TRABAJO EN N8N**

### **Flujo simplificado:**
```
🗓️ Trigger mensual (día 1)
    ↓
📡 GET /api/users/active/
    ↓
🔄 Para cada usuario:
    📡 GET /api/users/{id}/complete/
    🤖 IA procesa JSON completo
    📧 Email personalizado con reporte
```

### **Ventajas del enfoque:**
- ✅ **2 endpoints** en lugar de 7
- ✅ **1 llamada HTTP** por usuario en lugar de múltiples
- ✅ **IA con contexto completo** para análisis profundo
- ✅ **Flexibilidad total** para n8n (puede filtrar cualquier período)
- ✅ **Implementación simple** en Django

---

## 📂 **ESTRUCTURA DE ARCHIVOS A CREAR**

### **1. Crear directorio API:**
```
apps/expenses/api/
├── __init__.py
├── serializers.py
├── views.py
├── urls.py
└── authentication.py
```

### **2. Archivos principales:**

#### **`apps/expenses/api/authentication.py`**
```python
# Clase personalizada para autenticación Bearer Token
```

#### **`apps/expenses/api/serializers.py`**
```python
# Serializers para formatear los datos JSON
# - UserActiveSerializer
# - UserCompleteSerializer  
# - ExpenseSerializer
# - BudgetSerializer
```

#### **`apps/expenses/api/views.py`**
```python
# ViewSets con lógica de negocio
# - ActiveUsersView
# - UserCompleteView
```

#### **`apps/expenses/api/urls.py`**
```python
# URLs de la API
# - /api/users/active/
# - /api/users/<int:user_id>/complete/
```

### **3. Integración en URLs principales:**
```python
# config/urls.py
urlpatterns = [
    # ... urls existentes
    path('api/', include('apps.expenses.api.urls')),
]
```

---

## 🛠️ **PLAN DE IMPLEMENTACIÓN**

### **FASE 1: Setup básico** ⭐ **EMPEZAR AQUÍ**
1. ✅ Verificar DRF instalado (`djangorestframework==3.15.2`)
2. 🔨 Crear estructura de directorios `apps/expenses/api/`
3. 🔨 Implementar autenticación Bearer Token
4. 🔨 Crear endpoint básico `GET /api/users/active/`

### **FASE 2: Endpoint completo**
5. 🔨 Crear serializers para todos los modelos
6. 🔨 Implementar `GET /api/users/{id}/complete/`
7. 🔨 Optimizar queries (select_related, prefetch_related)
8. 🔨 Testing básico

### **FASE 3: Integración con n8n**
9. 🔨 Configurar URLs en `config/urls.py`
10. ✅ Testing completo con curl/Postman
11. ✅ Integración con workflow n8n existente
12. ✅ Documentación final

---

## 🧪 **TESTING**

### **Comandos de prueba:**

#### **Test de autenticación:**
```bash
# Sin token (debe fallar)
curl http://localhost:8000/api/users/active/

# Con token (debe funcionar)
curl -H "Authorization: Bearer dev-api-token-123" \
     http://localhost:8000/api/users/active/
```

#### **Test de endpoints:**
```bash
# Lista usuarios activos
curl -H "Authorization: Bearer dev-api-token-123" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/users/active/

# Datos completos de usuario
curl -H "Authorization: Bearer dev-api-token-123" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/users/1/complete/
```

---

## 🔒 **CONSIDERACIONES DE SEGURIDAD**

### **Tokens por ambiente:**
- 🔧 **Desarrollo:** `dev-api-token-123` (simple para testing)
- 🔐 **Producción:** Token seguro de 32+ caracteres en `.env.production`

### **Validaciones:**
- ✅ Verificar Bearer token en cada request
- ✅ Solo devolver datos del usuario autenticado
- ✅ Rate limiting (opcional para v1)
- ✅ CORS configurado para n8n

### **Variables de entorno necesarias:**
```bash
# .env.production
N8N_WEBHOOK_TOKEN=super-secure-webhook-token-32-chars
N8N_API_TOKEN=super-secure-api-token-32-chars-different
```

---

## 📈 **MÉTRICAS Y MONITORING**

### **Logs a implementar:**
- 📊 Requests por endpoint
- 📊 Tiempo de respuesta
- 📊 Errores de autenticación
- 📊 Usuarios consultados

### **Performance:**
- 🚀 Cache Redis (opcional para v2)
- 🚀 Pagination para usuarios con muchos gastos
- 🚀 Compresión GZIP
- 🚀 Optimización de queries

---

## 🎯 **EJEMPLO DE USO FINAL**

### **n8n obtiene usuarios activos:**
```http
GET /api/users/active/
Authorization: Bearer production-token-abc123

Response:
[
  {"id": 1, "username": "juan", "email": "juan@email.com"},
  {"id": 5, "username": "maria", "email": "maria@email.com"}
]
```

### **n8n obtiene datos de Juan:**
```http
GET /api/users/1/complete/  
Authorization: Bearer production-token-abc123

Response: 
{
  "user": {...},
  "budget": {...},
  "complete_history": {
    "all_expenses": [...], // 245 gastos
    "monthly_summaries": {...}
  }
}
```

### **IA genera reporte:**
```
"Hola Juan! En enero gastaste €450, un 10% menos que diciembre. 
Tu categoría principal fue delivery (€200). 
Patrón detectado: gastas más los fines de semana.
Proyección febrero: €480 si continúas la tendencia actual."
```

---

## ✅ **ESTADO ACTUAL**

- ✅ **DRF instalado** y listo
- ✅ **Autenticación Bearer** ya configurada para webhooks
- ✅ **Modelos optimizados** (Expense, Budget, Category, User)
- ✅ **Docker setup** funcionando
- 🔨 **API pendiente** de implementar

---

## 🚀 **SIGUIENTE PASO**

**Empezar con FASE 1:**
1. Crear directorio `apps/expenses/api/`
2. Implementar autenticación Bearer Token
3. Crear endpoint básico `GET /api/users/active/`

¡Listo para comenzar! 🎉 