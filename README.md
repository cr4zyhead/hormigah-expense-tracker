# �� Hormigah - Control Inteligente de Gastos Hormiga

<div align="center">

**Una aplicación web moderna para controlar esos pequeños gastos diarios que pasan desapercibidos pero que al final del año suman cantidades importantes.**

![Django](https://img.shields.io/badge/Django-5.2.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-1.9-336791?style=for-the-badge&logo=htmx&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

[🚀 Demo](#-instalación) • [📊 Características](#-características-principales) • [🏗️ Arquitectura](#️-arquitectura) • [🤝 Contribuir](#-contribuir)

</div>

---

## 🎯 ¿Qué son los "Gastos Hormiga"?

Los **gastos hormiga** son esos pequeños desembolsos cotidianos que individualmente parecen insignificantes, pero que acumulados pueden representar una parte considerable de nuestro presupuesto:

- ☕ **Café diario**: $3 × 365 días = $1,095 al año
- 🍕 **Delivery impulsivo**: $15 × 2 veces/semana = $1,560 al año  
- 🚗 **Taxis innecesarios**: $8 × 3 veces/semana = $1,248 al año
- 📱 **Suscripciones no usadas**: $10 × 12 meses = $120 al año

**¡Total: $4,023 al año en gastos "pequeños"!** 😱

---

## ✨ Características Principales

### 🏠 **Dashboard Inteligente**
- **Métricas en tiempo real** con filtros por período
- **Gráficos interactivos** (dona y líneas) con Chart.js
- **Auto-actualización** sin recargar página (HTMX)
- **Responsive design** optimizado para móviles

### 📊 **Análisis Visual**
- **Distribución por categorías** con colores personalizados
- **Tendencias temporales** para identificar patrones
- **Proyecciones anuales** automáticas
- **Comparativas mensuales** 

### ⚡ **Experiencia de Usuario Moderna**
- **Interfaz HTMX** sin recargas de página
- **Modales dinámicos** para CRUD completo
- **Auto-refresh** en listas y métricas
- **Navegación fluida** entre secciones

### 🔧 **Funcionalidades Avanzadas**
- **Filtros inteligentes** por fecha, categoría y monto
- **CRUD completo** con validación en tiempo real
- **Sistema de categorías** con colores personalizados
- **Gestión de usuarios** con autenticación segura

---

## 🚀 Instalación

### Requisitos Previos
- **Python 3.8+**
- **Git**

### Setup Rápido
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/hormigah.git
cd hormigah

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install django

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Cargar datos de ejemplo (opcional)
python manage.py loaddata apps/expenses/fixtures/categories.json

# 7. ¡Ejecutar la aplicación!
python manage.py runserver
```

### 🌐 Acceso
- **Aplicación principal**: http://127.0.0.1:8000/
- **Panel de administración**: http://127.0.0.1:8000/admin/

---

## 🏗️ Arquitectura

### 📁 Estructura del Proyecto
```
hormigah/
├── 🏠 apps/
│   ├── 🔧 core/                     # Utilidades base y templates
│   │   ├── templates/
│   │   │   ├── base.html           # Template base con Tailwind
│   │   │   ├── core/includes/      # Header y footer
│   │   │   └── registration/       # Autenticación
│   │   └── views.py                # Vistas compartidas
│   │
│   └── 💰 expenses/                 # App principal de gastos
│       ├── 📊 models.py            # Category y Expense
│       ├── 🎯 views.py             # Lógica de negocio
│       ├── 📝 forms.py             # Formularios con validación
│       ├── 🔗 urls.py              # Rutas de la aplicación
│       ├── 🛠️ utils/               # Utilidades modularizadas
│       │   ├── util_dashboard.py   # Métricas y dashboard
│       │   ├── util_chart_data.py  # Datos para gráficos
│       │   ├── util_expense_list.py # Filtros y listado
│       │   └── util_crud_operations.py # Operaciones CRUD + HTMX
│       ├── 🎨 templates/expenses/  # Templates especializados
│       ├── 📱 static/expenses/     # CSS y JS específicos
│       └── 🔄 migrations/          # Migraciones de BD
│
├── ⚙️ config/                      # Configuración Django
├── 🎨 static/                      # Archivos estáticos globales
│   ├── css/custom.css              # Estilos personalizados
│   └── js/dashboard.js             # JavaScript modularizado
├── 🗄️ db.sqlite3                   # Base de datos SQLite
└── 📋 manage.py                    # Script de gestión Django
```

### 🧩 Tecnologías Utilizadas

#### **Backend**
- **Django 5.2.3**: Framework web robusto
- **SQLite**: Base de datos ligera para desarrollo
- **Python 3.12**: Lenguaje base

#### **Frontend**
- **HTMX**: Interactividad sin JavaScript complejo
- **Tailwind CSS**: Framework de utilidades CSS
- **Chart.js**: Gráficos interactivos
- **Alpine.js**: Interactividad ligera

#### **Arquitectura**
- **Modular**: Utils organizados por responsabilidad
- **Responsive**: Diseño móvil-first
- **Progressive Enhancement**: Funciona sin JS, mejor con JS

---

## 🎮 Uso de la Aplicación

### 1. **Dashboard Principal**
```
🐜 Dashboard de Gastos
├── 📊 Métricas del período seleccionado
├── 🍩 Gráfico de distribución por categorías  
├── 📈 Tendencia temporal de gastos
└── 🕐 Lista de gastos recientes
```

### 2. **Gestión de Gastos**
```
💰 Operaciones CRUD
├── ➕ Agregar nuevo gasto (modal HTMX)
├── ✏️ Editar gasto existente (modal HTMX)
├── 🗑️ Eliminar gasto (confirmación)
└── 👁️ Ver detalles completos
```

### 3. **Filtros Avanzados**
```
🔍 Sistema de Filtros
├── 📅 Por período (Este mes, último mes, últimos 7/30 días)
├── 🏷️ Por categoría (Café, Delivery, Transporte, etc.)
├── 📅 Por rango de fechas personalizado
└── 💵 Por rango de montos (min/max)
```

---

## 🔥 Funcionalidades Destacadas

### ⚡ **Auto-Refresh Inteligente**
- Las listas se actualizan automáticamente al crear/editar gastos
- Dashboard se recarga automáticamente tras cambios
- Sin necesidad de recargar la página manualmente

### 🎨 **Interfaz Moderna**
- **Modales HTMX**: Operaciones sin cambiar de página
- **Indicadores de carga**: Feedback visual durante operaciones
- **Mensajes de éxito**: Confirmación clara de acciones
- **Estados vacíos**: Guías útiles cuando no hay datos

### 📱 **Responsive Design**
- **Mobile-first**: Optimizado para dispositivos móviles
- **Navegación adaptativa**: Menú hamburguesa en móviles
- **Tablas responsivas**: Scroll horizontal cuando es necesario
- **Touch-friendly**: Botones y controles optimizados para tocar

---

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Test específicos de expenses
python manage.py test apps.expenses

# Verificar configuración
python manage.py check
```

---

## 🚀 Deploy en Producción

### Variables de Entorno Necesarias
```bash
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgres://user:pass@host:port/db
```

### Configuración de Archivos Estáticos
```bash
# Recopilar archivos estáticos
python manage.py collectstatic

# Configurar servidor web (Nginx/Apache)
# Servir archivos estáticos directamente
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 

### 🐛 Reportar Bugs
- Usar el [sistema de issues](../../issues)
- Incluir pasos para reproducir
- Especificar entorno (OS, Python, Django)

### ✨ Proponer Features
- Describir el caso de uso
- Explicar el beneficio para usuarios
- Considerar impacto en UX

### 🔧 Pull Requests
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit con conventional commits
4. Push y crear PR

---

## 📝 Conventional Commits

Este proyecto usa [Conventional Commits](https://conventionalcommits.org/):

```bash
feat: agregar filtro por rango de fechas
fix: corregir auto-refresh en dashboard  
docs: actualizar README con nuevas funcionalidades
refactor: modularizar utils en archivos especializados
style: mejorar responsive design en móviles
test: agregar tests para filtros avanzados
```

---


## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Django Team** por el framework increíble
- **HTMX** por simplificar la interactividad web
- **Tailwind CSS** por el sistema de diseño
- **Chart.js** por los gráficos hermosos

---

<div align="center">

**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

**Desarrollado con ❤️ para ayudarte a controlar tus gastos hormiga**

</div> 