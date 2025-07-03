# Hormigah - Control Inteligente de Gastos Hormiga

Una aplicación web moderna para controlar esos pequeños gastos diarios que pasan desapercibidos pero que al final del año suman cantidades importantes.

![Django](https://img.shields.io/badge/Django-5.2.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-1.9-336791?style=for-the-badge&logo=htmx&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

## Concepto: Gastos Hormiga

Los **gastos hormiga** son pequeños desembolsos cotidianos que individualmente parecen insignificantes, pero acumulados representan una parte considerable del presupuesto:

- Café diario: $3 × 365 días = $1,095 al año
- Delivery impulsivo: $15 × 2 veces/semana = $1,560 al año  
- Taxis innecesarios: $8 × 3 veces/semana = $1,248 al año
- Suscripciones no usadas: $10 × 12 meses = $120 al año

**Total: $4,023 al año en gastos "pequeños"**

## Características Principales

### Dashboard Inteligente
- Métricas en tiempo real con filtros por período
- Gráficos interactivos (dona y líneas) con Chart.js
- Auto-actualización sin recargar página (HTMX)
- Diseño responsive optimizado para móviles

### Análisis Visual
- Distribución por categorías con colores personalizados
- Tendencias temporales para identificar patrones
- Proyecciones anuales automáticas
- Comparativas mensuales

### Experiencia de Usuario
- Interfaz HTMX sin recargas de página
- Modales dinámicos para operaciones CRUD
- Auto-refresh en listas y métricas
- Navegación fluida entre secciones

### Funcionalidades Avanzadas
- Filtros inteligentes por fecha, categoría y monto
- CRUD completo con validación en tiempo real
- Sistema de categorías con colores personalizados
- Gestión de usuarios con autenticación segura
- Sistema de alertas de presupuesto automatizado

## Tecnologías

### Backend
- **Django 5.2.3**: Framework web robusto
- **PostgreSQL**: Base de datos para desarrollo y producción
- **Python 3.12**: Lenguaje base
- **Gunicorn**: Servidor WSGI para producción

### Frontend
- **HTMX**: Interactividad sin JavaScript complejo
- **Tailwind CSS**: Framework de utilidades CSS
- **Chart.js**: Gráficos interactivos
- **Alpine.js**: Interactividad ligera

### Infraestructura
- **Docker**: Containerización completa
- **Nginx**: Servidor web y proxy inverso
- **n8n**: Automatización de workflows y reportes (opcional)

## Instalación

### Requisitos Previos
- Docker y Docker Compose
- Git

### Setup Rápido
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/hormigah.git
cd hormigah

# Configurar variables de entorno
cp .env.example .env.local

# Iniciar aplicación
docker-compose up -d

# Configurar Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Acceso
- **Aplicación principal**: http://localhost:8000/
- **Panel de administración**: http://localhost:8000/admin/

## Estructura del Proyecto

```
hormigah/
├── apps/
│   ├── core/                     # Utilidades base y templates
│   ├── expenses/                 # App principal de gastos
│   │   ├── models.py            # Category y Expense
│   │   ├── views.py             # Lógica de negocio
│   │   ├── forms.py             # Formularios con validación
│   │   ├── utils/               # Utilidades modularizadas
│   │   ├── templates/           # Templates especializados
│   │   └── static/              # CSS y JS específicos
│   └── users/                   # Gestión de usuarios
├── config/                      # Configuración Django
│   ├── settings/                # Settings modulares
│   │   ├── base.py             # Configuración base
│   │   ├── local.py            # Desarrollo
│   │   └── production.py       # Producción
│   └── urls.py                 # URLs principales
├── static/                      # Archivos estáticos globales
├── docker-compose.yml           # Docker desarrollo
├── docker-compose.prod.yml      # Docker producción
├── Dockerfile                   # Imagen de la aplicación
└── requirements.txt             # Dependencias Python
```

## Uso de la Aplicación

### Dashboard Principal
- Métricas del período seleccionado
- Gráfico de distribución por categorías  
- Tendencia temporal de gastos
- Lista de gastos recientes

### Gestión de Gastos
- Agregar nuevo gasto (modal HTMX)
- Editar gasto existente (modal HTMX)
- Eliminar gasto (confirmación)
- Ver detalles completos

### Filtros Avanzados
- Por período (Este mes, último mes, últimos 7/30 días)
- Por categoría (Café, Delivery, Transporte, etc.)
- Por rango de fechas personalizado
- Por rango de montos (min/max)

### Sistema de Alertas
- Alertas automáticas al alcanzar el 90% del presupuesto mensual
- Configuración por usuario (activar/desactivar)
- Integración con n8n para automatización de notificaciones

## Comandos Útiles

### Desarrollo
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Ejecutar migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Ejecutar tests
docker-compose exec web python manage.py test

# Acceder a Django shell
docker-compose exec web python manage.py shell
```

### Producción
```bash
# Desplegar en producción
docker-compose -f docker-compose.prod.yml up -d

# Ver estado de servicios
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs web
```

## Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Tests específicos de expenses
python manage.py test apps.expenses

# Verificar configuración
python manage.py check
```

## Arquitectura

### Patrones de Diseño
- **Modular**: Utils organizados por responsabilidad
- **Responsive**: Diseño móvil-first
- **Progressive Enhancement**: Funciona sin JS, mejor con JS
- **Containerizada**: Docker-first development y deployment

### Funcionalidades Destacadas
- **Auto-Refresh Inteligente**: Las listas se actualizan automáticamente
- **Interfaz Moderna**: Modales HTMX sin cambiar de página
- **Responsive Design**: Optimizado para todos los dispositivos
- **Sistema de Automatización**: Integración con n8n para reportes y alertas

## Contribuir

### Reportar Bugs
- Usar el sistema de issues
- Incluir pasos para reproducir
- Especificar entorno (OS, Python, Django)

### Proponer Features
- Describir el caso de uso
- Explicar el beneficio para usuarios
- Considerar impacto en UX

### Pull Requests
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit con conventional commits
4. Push y crear PR

## Conventional Commits

Este proyecto usa [Conventional Commits](https://conventionalcommits.org/):

```bash
feat: agregar filtro por rango de fechas
fix: corregir auto-refresh en dashboard  
docs: actualizar README con nuevas funcionalidades
refactor: modularizar utils en archivos especializados
style: mejorar responsive design en móviles
test: agregar tests para filtros avanzados
```

## Licencia

Este proyecto está bajo la **Licencia MIT**. Ver [LICENSE](LICENSE) para más detalles.

## Agradecimientos

- Django Team por el framework increíble
- HTMX por simplificar la interactividad web
- Tailwind CSS por el sistema de diseño
- Chart.js por los gráficos hermosos