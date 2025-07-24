# N8N Workflows

Este directorio contiene los workflows de automatización para la aplicación Gastos Hormiga.

## Workflows Disponibles

### Budget Alert Emails
**Archivo:** `Budget Alert Emails.json`

Workflow que envía alertas por email cuando el usuario supera ciertos porcentajes de su presupuesto mensual.

**Funcionalidad:**
- Recibe webhooks con datos de gastos del usuario
- Envía emails automáticos con alertas de presupuesto
- Incluye detalles del gasto actual y porcentaje utilizado

**Nodos:**
- Webhook: Recibe datos de la aplicación Django
- Gmail: Envía el email de alerta al usuario

### Monthly Report
**Archivo:** `monthly report.json`

Workflow programado que genera reportes mensuales automáticos para todos los usuarios activos.

**Funcionalidad:**
- Se ejecuta automáticamente el día 1 de cada mes a las 9:00 AM
- Obtiene lista de usuarios activos desde la API
- Procesa gastos del mes anterior para cada usuario
- Genera análisis personalizado usando OpenAI
- Envía reporte por email con métricas y recomendaciones

**Nodos:**
- Schedule Trigger: Programación mensual
- HTTP Request: Obtiene usuarios y datos de gastos
- Code: Procesa y filtra datos del mes anterior
- OpenAI: Genera análisis personalizado
- Gmail: Envía reporte por email

## Configuración

Después de importar los workflows en n8n:

### 1. Configurar URLs en nodos HTTP Request
- Abrir nodo "Get Active Users" → cambiar URL por tu dominio real
- Abrir nodo "Get User Details" → cambiar URL por tu dominio real

### 2. Crear credenciales en n8n
Ir a Credenciales → Crear nuevas:
- **Gmail OAuth2** para envío de emails
- **OpenAI API** para análisis con IA  
- **Header Authentication** para webhooks

### 3. Actualizar tokens de autenticación
En nodos HTTP Request → Headers → Authorization:
- Reemplazar `YOUR_API_TOKEN_HERE` con tu Bearer token real

### 4. Personalizar emails
En nodo "Send Report Email" → Message:
- Cambiar `your-app@example.com` por tu email real

## Uso

1. Importa los archivos JSON en tu instancia de n8n
2. Configura las credenciales requeridas
3. Actualiza las URLs y tokens con tus valores reales
4. Activa los workflows 