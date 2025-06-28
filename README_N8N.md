# n8n - Automatización para Gastos Hormiga

<div align="center">

**Automatiza reportes, alertas y integraciones para tu aplicación de control de gastos**

![n8n](https://img.shields.io/badge/n8n-1.99.1-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

## ¿Qué es n8n?

**n8n** es una herramienta de automatización de workflows que te permite conectar diferentes servicios y automatizar tareas sin escribir código. En el contexto de Gastos Hormiga, n8n te permite:

- 📧 **Enviar reportes automáticos** de gastos por email
- 🚨 **Crear alertas** cuando superes presupuestos
- 📊 **Generar informes** mensuales automáticamente
- 🔗 **Integrar** con servicios externos (Gmail, Slack, Telegram, etc.)
- 💾 **Automatizar backups** de datos

---

## Acceso a n8n

### Desarrollo Local
- **URL**: http://localhost:5678/
- **Primera vez**: Crear usuario administrador

### Producción
- **URL**: https://tu-dominio.com/n8n/
- **Configuración**: Ya incluida en nginx y docker-compose

---

## Configuración Inicial

### 1. Primer Acceso

Al acceder por primera vez a n8n, necesitarás:

1. **Crear cuenta de administrador**:
   - Email: Tu email personal
   - Nombre y apellido
   - Contraseña segura (8+ caracteres, número, mayúscula)

2. **Configuración recomendada**:
   - ✅ Activar notificaciones de seguridad
   - ✅ Permitir telemetría (opcional)

### 2. Configuración de Credenciales

Para usar n8n con servicios externos, necesitarás configurar credenciales:

#### **Gmail (Para reportes por email)**
1. **Ir a**: Credenciales → Agregar credencial → Gmail
2. **Configurar**:
   - Usar OAuth2 (recomendado)
   - Autorizar acceso a tu cuenta Gmail
3. **Guardar** con nombre descriptivo: "Gmail Reportes"

#### **HTTP Request (Para Django API)**
1. **Ir a**: Credenciales → Agregar credencial → HTTP Request Auth
2. **Configurar**:
   - Tipo: Header Auth
   - Nombre: `Authorization`
   - Valor: `Bearer tu-api-token` (si usas autenticación)

---

## Workflows Predefinidos

### 🔄 **Workflow 1: Reporte Mensual Automático**

**Función**: Envía un email con resumen de gastos cada primer día del mes

**Nodos**:
1. **Cron** → `0 9 1 * *` (1 de cada mes a las 9:00 AM)
2. **HTTP Request** → Django API para obtener gastos del mes anterior
3. **Code** → Procesar datos y crear resumen HTML
4. **Gmail** → Enviar email con el reporte

**Datos incluidos**:
- Total gastado del mes anterior
- Distribución por categorías
- Comparación con mes anterior
- Top 5 gastos más altos

### 📊 **Workflow 2: Alerta de Presupuesto**

**Función**: Notifica cuando el gasto mensual supera el 80% del presupuesto

**Nodos**:
1. **Webhook** → Recibe notificación desde Django cuando se agrega gasto
2. **HTTP Request** → Obtener total del mes actual
3. **Code** → Calcular porcentaje del presupuesto
4. **If** → ¿Supera 80%?
5. **Gmail/Slack** → Enviar alerta

### 📈 **Workflow 3: Backup Semanal**

**Función**: Crea backup de datos cada domingo

**Nodos**:
1. **Cron** → `0 3 * * 0` (Domingos a las 3:00 AM)
2. **HTTP Request** → Exportar datos desde Django
3. **Google Drive** → Guardar backup en la nube
4. **Gmail** → Notificar backup completado

---

## APIs de Django Disponibles

### **Endpoints para n8n**

#### **Obtener Gastos**
```http
GET /api/expenses/
```
**Parámetros**:
- `start_date`: Fecha inicio (YYYY-MM-DD)
- `end_date`: Fecha fin (YYYY-MM-DD)
- `category`: ID de categoría (opcional)

**Respuesta**:
```json
{
  "expenses": [
    {
      "id": 1,
      "amount": "15.50",
      "description": "Café Starbucks",
      "category": "Café",
      "date": "2024-01-15"
    }
  ],
  "total": "15.50",
  "count": 1
}
```

#### **Obtener Resumen Mensual**
```http
GET /api/expenses/monthly-summary/
```
**Parámetros**:
- `year`: Año (2024)
- `month`: Mes (1-12)

**Respuesta**:
```json
{
  "month": "2024-01",
  "total": "456.78",
  "categories": {
    "Café": "125.50",
    "Delivery": "231.28",
    "Transporte": "100.00"
  },
  "comparison": {
    "previous_month": "390.45",
    "difference": "66.33",
    "percentage": "+17%"
  }
}
```

#### **Webhooks**
```http
POST /api/webhooks/expense-created/
POST /api/webhooks/budget-threshold/
```

---

## Ejemplos de Código para n8n

### **Procesar Datos de Django (Code Node)**

```javascript
// Procesar datos de gastos para reporte
const expenses = $input.first().json.expenses;
const total = $input.first().json.total;

// Agrupar por categoría
const byCategory = {};
expenses.forEach(expense => {
  if (!byCategory[expense.category]) {
    byCategory[expense.category] = 0;
  }
  byCategory[expense.category] += parseFloat(expense.amount);
});

// Crear HTML para email
const html = `
<h2>Reporte Mensual de Gastos</h2>
<p><strong>Total gastado:</strong> $${total}</p>
<h3>Por categorías:</h3>
<ul>
${Object.entries(byCategory).map(([cat, amount]) => 
  `<li>${cat}: $${amount.toFixed(2)}</li>`
).join('')}
</ul>
`;

return {
  json: {
    html: html,
    total: total,
    categories: byCategory
  }
};
```

### **Calcular Porcentaje de Presupuesto**

```javascript
// Configuración
const MONTHLY_BUDGET = 1000; // Tu presupuesto mensual

// Datos del webhook
const currentTotal = $input.first().json.total;
const percentage = (currentTotal / MONTHLY_BUDGET) * 100;

// Determinar acción
let shouldAlert = false;
let alertLevel = '';

if (percentage >= 100) {
  shouldAlert = true;
  alertLevel = 'CRÍTICO';
} else if (percentage >= 80) {
  shouldAlert = true;
  alertLevel = 'ADVERTENCIA';
}

return {
  json: {
    percentage: percentage.toFixed(1),
    shouldAlert: shouldAlert,
    alertLevel: alertLevel,
    currentTotal: currentTotal,
    budget: MONTHLY_BUDGET,
    remaining: MONTHLY_BUDGET - currentTotal
  }
};
```

---

## Integraciones Populares

### 📧 **Email (Gmail)**
- **Reportes automáticos**: Resúmenes mensuales
- **Alertas de presupuesto**: Notificaciones inmediatas
- **Confirmaciones**: Backup completado, etc.

### 💬 **Slack/Discord**
- **Notificaciones en tiempo real**: Gastos grandes
- **Reportes en canal**: Resúmenes diarios/semanales
- **Alertas de equipo**: Si compartes presupuesto

### 📱 **Telegram**
- **Bot personal**: Comandos para consultar gastos
- **Alertas móviles**: Notificaciones push
- **Reportes rápidos**: Resúmenes por comando

### ☁️ **Google Drive/Dropbox**
- **Backup automático**: Datos semanales
- **Reportes en PDF**: Guardar automáticamente
- **Sincronización**: Compartir con familia/contador

### 📊 **Google Sheets**
- **Datos en tiempo real**: Sincronizar gastos
- **Análisis avanzado**: Pivots y gráficos
- **Reportes visuales**: Para presentaciones

---

## Configuración de Webhooks en Django

### **Habilitar Webhooks**

#### **1. Agregar URLs en Django** (Opcional - para implementar)
```python
# urls.py
urlpatterns = [
    path('api/webhooks/expense-created/', WebhookExpenseView.as_view()),
]
```

#### **2. Configurar n8n Webhook**
1. **Crear workflow** con nodo "Webhook"
2. **Copiar URL**: http://localhost:5678/webhook/tu-id-unico
3. **Configurar en Django**: Enviar POST a esa URL cuando se cree gasto

### **Datos del Webhook**
```json
{
  "event": "expense_created",
  "expense": {
    "id": 123,
    "amount": "25.50",
    "description": "Almuerzo",
    "category": "Delivery",
    "date": "2024-01-15"
  },
  "month_total": "456.78",
  "user": "tu_usuario"
}
```

---

## Troubleshooting

### **Problema: n8n no carga**
```bash
# Verificar estado del contenedor
docker-compose ps

# Ver logs de n8n
docker logs gastos_hormiga_n8n_prod --tail 20

# Reiniciar n8n
docker-compose restart n8n
```

### **Problema: No puede conectar con Django**
1. **Verificar URL**: Usar `http://web:8000` (no localhost)
2. **Network**: n8n y Django deben estar en la misma red Docker
3. **Firewall**: Verificar puertos abiertos

### **Problema: Credenciales de Gmail**
1. **Activar 2FA** en tu cuenta Google
2. **Crear App Password** específica para n8n
3. **Usar SMTP** en lugar de OAuth si persisten problemas

### **Problema: Workflows no se ejecutan**
1. **Verificar Cron**: Sintaxis correcta
2. **Activar Workflow**: Debe estar en estado "Active"
3. **Logs de ejecución**: Revisar en n8n → Executions

---

## Seguridad y Buenas Prácticas

### **🔒 Seguridad**
- **Usuario único**: Solo crear una cuenta administrador
- **Contraseña fuerte**: Usar gestor de contraseñas
- **HTTPS**: Siempre usar SSL en producción
- **Firewall**: n8n solo accesible por ti

### **📋 Buenas Prácticas**
- **Nombres descriptivos**: Para workflows y credenciales
- **Documentación**: Agregar notas en workflows complejos
- **Testing**: Probar workflows antes de activar
- **Monitoreo**: Revisar ejecuciones periódicamente

### **💾 Backup de n8n**
```bash
# Backup de datos de n8n
docker run --rm -v gastos_hormiga_n8n_data_prod:/data -v $(pwd):/backup ubuntu tar czf /backup/n8n_backup.tar.gz -C /data .

# Restaurar backup
docker run --rm -v gastos_hormiga_n8n_data_prod:/data -v $(pwd):/backup ubuntu tar xzf /backup/n8n_backup.tar.gz -C /data
```

---

## Workflows Avanzados

### **🤖 Análisis Inteligente de Gastos**
```
Cron (diario) → Django API → AI/ML Processing → Insights Email
```

### **📊 Dashboard en Tiempo Real**
```
Webhook → Process Data → Update Google Sheets → Slack Notification
```

### **💰 Optimizer de Gastos**
```
Monthly Trigger → Analyze Patterns → Generate Recommendations → Email Report
```

---

## Recursos Adicionales

### **Documentación Oficial**
- [n8n Documentation](https://docs.n8n.io/)
- [Workflow Templates](https://n8n.io/workflows/)
- [Node Reference](https://docs.n8n.io/nodes/)

### **Tutoriales Recomendados**
- [Primeros pasos con n8n](https://docs.n8n.io/getting-started/)
- [Webhooks avanzados](https://docs.n8n.io/nodes/n8n-nodes-base.webhook/)
- [Email automation](https://docs.n8n.io/nodes/n8n-nodes-base.gmail/)

### **Comunidad**
- [n8n Community](https://community.n8n.io/)
- [Discord Server](https://discord.gg/n8n)
- [GitHub](https://github.com/n8n-io/n8n)

---

## Soporte

### **Problemas con n8n**
1. **Documentación oficial**: Primera referencia
2. **Community forum**: Para preguntas específicas
3. **GitHub Issues**: Para bugs confirmados

### **Problemas de Integración**
- **Django API**: Revisar logs de la aplicación
- **Docker Network**: Verificar conectividad entre contenedores
- **Nginx Proxy**: Comprobar configuración de rutas

---

<div align="center">

**¡Automatiza tus gastos y ahorra tiempo! 🚀**

*Desarrollado con ❤️ para hacer tu control de gastos más inteligente*

</div> 