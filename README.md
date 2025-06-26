# Hormigah - Control Inteligente de Gastos Hormiga

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
- **Docker** y **Docker Compose**
- **Git**

### 🚀 Setup Rápido con Docker
```bash
# 1. Clonar e iniciar
git clone https://github.com/tu-usuario/hormigah.git
cd hormigah

# 2. Configurar y ejecutar
cp .env.example .env.local
docker-compose up -d

# 3. ¡Listo! Tu app está en http://localhost:8000
```

## 🔒 Configuración SSL/HTTPS (Producción)

### Dominio con DuckDNS
1. Crear cuenta en [DuckDNS](https://duckdns.org)
2. Configurar dominio: `tuapp.duckdns.org` → `tu-servidor-ip`

### Certificado SSL
```bash
# En tu servidor
sudo apt update && sudo apt install certbot
sudo certbot certonly --standalone -d tuapp.duckdns.org
```

### Variables adicionales en .env.production
```bash
# Dominios permitidos
ALLOWED_HOSTS=tu-servidor-ip,localhost,tuapp.duckdns.org

# Orígenes de confianza CSRF  
CSRF_TRUSTED_ORIGINS=https://tuapp.duckdns.org,http://tu-servidor-ip

# Configuraciones de seguridad SSL
SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

### Deployment con SSL
```bash
# Montar certificados y reiniciar
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

### 🔧 Configuración Completa
```bash
# Crear superusuario (para admin)
docker-compose exec web python manage.py createsuperuser

# Cargar datos de ejemplo (opcional)
docker-compose exec web python manage.py loaddata apps/expenses/fixtures/categories.json
```

### 🐍 Setup Manual (Alternativo)
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/hormigah.git
cd hormigah

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py migrate
python manage.py createsuperuser

# 5. Ejecutar aplicación
python manage.py runserver
```

### 🌐 Acceso
- **Aplicación principal**: http://localhost:8000/
- **Panel de administración**: http://localhost:8000/admin/

> 💡 **Para deployment en producción**, consulta [README_DOCKER.md](README_DOCKER.md)

---

## 🐳 Comandos Docker

### 📋 Comandos Docker Estándar

#### **Desarrollo**
```bash
# Iniciar aplicación
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Parar aplicación
docker-compose down

# Ejecutar comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
```

#### **Producción**
```bash
# Desplegar en producción
docker-compose -f docker-compose.prod.yml up -d

# Ver estado de servicios
docker-compose -f docker-compose.prod.yml ps

# Backup de base de datos
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres gastos_hormiga_prod > backup.sql
```

### 🚀 Scripts Helper (Alternativa)

> 💡 **Opcional**: También puedes usar scripts que simplifican las operaciones más comunes

#### **Desarrollo Local**
```bash
# Setup inicial
cp .env.example .env.local
./scripts/docker-dev.sh build
./scripts/docker-dev.sh up

# Configurar Django
./scripts/docker-dev.sh migrate
./scripts/docker-dev.sh createsuperuser

# Desarrollo día a día
./scripts/docker-dev.sh makemigrations
./scripts/docker-dev.sh migrate
./scripts/docker-dev.sh test

# Utilidades
./scripts/docker-dev.sh logs          # Ver logs
./scripts/docker-dev.sh shell         # Django shell
./scripts/docker-dev.sh bash          # Bash en contenedor
./scripts/docker-dev.sh down          # Parar servicios
./scripts/docker-dev.sh clean         # Limpiar sistema
```

#### **Producción**
```bash
# Deployment
./scripts/docker-prod.sh build
./scripts/docker-prod.sh up

# Mantenimiento
./scripts/docker-prod.sh migrate
./scripts/docker-prod.sh collectstatic

# Monitoreo
./scripts/docker-prod.sh status       # Estado de servicios
./scripts/docker-prod.sh logs         # Ver logs
./scripts/docker-prod.sh backup       # Backup de BD

# Actualizaciones
./scripts/docker-prod.sh update       # Pull, build y restart
```

### 🔧 Workflow de Deployment

#### **En el Servidor de Producción**
```bash
# 1. Conectar al servidor
ssh root@tu-servidor-ip
cd /ruta/a/tu/aplicacion

# 2. Actualizar código
git pull origin main

# 3. Actualizar aplicación
./scripts/docker-prod.sh update

# 4. Verificar estado
./scripts/docker-prod.sh status
```

#### **Monitoreo Continuo**
```bash
# Ver estado general
./scripts/docker-prod.sh status

# Revisar logs por errores
./scripts/docker-prod.sh logs

# Verificar salud de la aplicación
./scripts/docker-prod.sh logs web
```

> 📚 **Documentación completa con más workflows**: [README_DOCKER.md](README_DOCKER.md)

### 💡 Características de los Scripts

Los scripts incluyen algunas características adicionales:

- **Comandos más cortos**: `./scripts/docker-dev.sh up` vs `docker-compose up -d`
- **Validaciones automáticas**: Verifican dependencias antes de ejecutar
- **Feedback visual**: Mensajes con colores para mejor legibilidad
- **Operaciones combinadas**: Como `update` que incluye pull, build y restart

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
│       ├── 🎨 templates/expenses/  # Templates especializados
│       ├── 📱 static/expenses/     # CSS y JS específicos
│       └── 🔄 migrations/          # Migraciones de BD
│
├── ⚙️ config/                      # Configuración Django
│   ├── settings/                   # Settings modulares
│   │   ├── base.py                 # Configuración base
│   │   ├── local.py                # Desarrollo
│   │   └── production.py           # Producción
│   ├── urls.py                     # URLs principales
│   ├── wsgi.py                     # WSGI para producción
│   └── asgi.py                     # ASGI para async
│
├── 🐳 docker/                      # Configuración Docker
│   ├── nginx.conf                  # Configuración Nginx
│   └── entrypoint.sh               # Script de inicialización
│
├── 🎨 static/                      # Archivos estáticos globales
│   ├── css/custom.css              # Estilos personalizados
│   └── js/dashboard.js             # JavaScript modularizado
│
├── 📋 docker-compose.yml           # Docker desarrollo
├── 📋 docker-compose.prod.yml      # Docker producción  
├── 🐋 Dockerfile                   # Imagen de la aplicación
├── 📝 .env.example                 # Variables de entorno ejemplo
├── 📚 README_DOCKER.md             # Documentación Docker
├── 🗄️ requirements.txt             # Dependencias Python
└── 📋 manage.py                    # Script de gestión Django
```

### 🧩 Tecnologías Utilizadas

#### **Backend**
- **Django 5.2.3**: Framework web robusto
- **PostgreSQL**: Base de datos para desarrollo y producción
- **Python 3.12**: Lenguaje base
- **Gunicorn**: Servidor WSGI para producción

#### **Frontend**
- **HTMX**: Interactividad sin JavaScript complejo
- **Tailwind CSS**: Framework de utilidades CSS
- **Chart.js**: Gráficos interactivos
- **Alpine.js**: Interactividad ligera

#### **Infraestructura**
- **Docker**: Containerización completa
- **Nginx**: Servidor web y proxy inverso
- **PostgreSQL**: Base de datos principal
- **Redis**: Cache (opcional)

#### **Arquitectura**
- **Modular**: Utils organizados por responsabilidad
- **Responsive**: Diseño móvil-first
- **Progressive Enhancement**: Funciona sin JS, mejor con JS
- **Containerizada**: Docker-first development y deployment
- **Multi-ambiente**: Configuraciones separadas dev/prod

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