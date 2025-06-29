# Gastos Hormiga - Configuración Docker

## Introducción

Esta aplicación Django ha sido configurada para ejecutarse con Docker y PostgreSQL. Incluye configuraciones separadas para desarrollo y producción.

## Comandos Docker Compose

Esta aplicación utiliza **Docker Compose** para gestionar los servicios. Usa los comandos estándar según el entorno:

## Arquitectura

### Desarrollo (`docker-compose.yml`)
- **web**: Aplicación Django con hot reload
- **db**: PostgreSQL 15
- **n8n**: Herramienta de automatización de workflows

### Producción (`docker-compose.prod.yml`)
- **web**: Aplicación Django con Gunicorn
- **db**: PostgreSQL 15
- **nginx**: Servidor web y proxy inverso
- **n8n**: Automatización y reportes (accesible via /n8n/)

## Primeros Pasos

### 1. Prerrequisitos
```bash
docker --version
docker-compose --version
```

### 2. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo como .env.local
cp .env.example .env.local
```

**Estructura de Archivos:**
- `.env.example` - Plantilla con instrucciones
- `.env.local` - Variables para desarrollo
- `.env.production` - Variables para producción

### 3. Iniciar en Desarrollo
```bash
# Construir e iniciar servicios
docker-compose build
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate
```

### 4. Crear Superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Acceder a la Aplicación
- **Aplicación**: http://localhost:8000
- **Panel Admin**: http://localhost:8000/admin
- **n8n (Automatizaciones)**: http://localhost:5678

## Comandos de Desarrollo

### Docker Compose
```bash
# Construir e iniciar
docker-compose build
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down
```

### Django
```bash
# Migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Archivos estáticos
docker-compose exec web python manage.py collectstatic

# Shell
docker-compose exec web python manage.py shell

# Tests
docker-compose exec web python manage.py test
```

### n8n
```bash
# Ver logs de n8n
docker-compose logs -f n8n

# Reiniciar n8n
docker-compose restart n8n

# Acceder al contenedor n8n
docker-compose exec n8n sh
```

### Base de Datos
```bash
# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d gastos_hormiga_dev

# Backup
docker-compose exec db pg_dump -U postgres gastos_hormiga_dev > backup.sql

# Restaurar
docker-compose exec -T db psql -U postgres -d gastos_hormiga_dev < backup.sql
```

## Configuración de Producción

### 1. Variables de Entorno
```bash
# Copiar y configurar para producción
cp .env.example .env.production

# Editar valores importantes:
# SECRET_KEY=clave-super-segura
# DEBUG=False
# DB_PASSWORD=contraseña-segura
# ALLOWED_HOSTS=tu-dominio.com
```

### 2. Iniciar en Producción
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Estructura de Archivos

```
.
├── docker/
│   ├── nginx.conf          # Configuración Nginx
│   └── entrypoint.sh       # Script de entrada
├── config/settings/
│   ├── base.py             # Configuración base
│   ├── local.py            # Desarrollo
│   └── production.py       # Producción
├── docker-compose.yml      # Desarrollo
├── docker-compose.prod.yml # Producción
├── Dockerfile              # Imagen Django
├── .env.example           # Plantilla variables
├── .env.local             # Variables desarrollo
├── .env.production        # Variables producción
└── README_N8N.md          # Documentación n8n
```

## Variables de Entorno

### Desarrollo (.env.local)
```bash
SECRET_KEY=clave-desarrollo
DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.local
DB_NAME=gastos_hormiga_dev
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# n8n
N8N_HOST=localhost
N8N_PROTOCOL=http
```

> **Para configurar automatizaciones con n8n**, consulta [README_N8N.md](README_N8N.md)

### Producción (.env.production)
```bash
SECRET_KEY=clave-super-segura-produccion
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DB_NAME=gastos_hormiga_prod
DB_USER=postgres_user
DB_PASSWORD=contraseña-super-segura
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

## Seguridad

### Usuarios Administrativos

**Desarrollo:**
- Username: cualquier nombre
- Password: puede ser simple

**Producción:**
- Username: NO uses admin, root, administrator
- Password: mínimo 12 caracteres, números y símbolos
- Email: dirección real para recuperación

## Solución de Problemas

### Error de Conexión a Base de Datos
```bash
docker-compose ps
docker-compose logs db
docker-compose restart
```

### Limpiar y Reiniciar
```bash
docker-compose down -v
docker system prune -f
docker-compose build --no-cache
docker-compose up -d
```

## Monitoreo

### Logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo Django
docker-compose logs -f web
```

### Acceso a Contenedores
```bash
# Shell Django
docker-compose exec web python manage.py shell

# Bash
docker-compose exec web bash

# PostgreSQL
docker-compose exec db psql -U postgres -d gastos_hormiga_dev
```

## Workflows Completos

### Desarrollo Local - Primer Setup
```bash
# 1. Configurar entorno
cp .env.example .env.local

# 2. Construir e iniciar
docker-compose build
docker-compose up -d

# 3. Configurar Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# 4. ¡Listo! Aplicación disponible en http://localhost:8000
```

### Desarrollo Local - Día a Día
```bash
# Iniciar trabajo
docker-compose up -d

# Crear/aplicar migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Ejecutar tests
docker-compose exec web python manage.py test

# Ver logs si hay problemas
docker-compose logs -f web

# Terminar trabajo
docker-compose down
```

### Deployment en Producción
```bash
# 1. Preparar servidor
ssh root@tu-servidor-ip
cd /ruta/a/tu/aplicacion

# 2. Configurar entorno
cp .env.example .env.production
# Editar .env.production con valores seguros

# 3. Deploy inicial
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 4. Verificar estado
docker-compose -f docker-compose.prod.yml ps
```

### Actualización en Producción
```bash
# 1. Conectar al servidor
ssh root@tu-servidor-ip
cd /ruta/a/tu/aplicacion

# 2. Actualizar código
git pull origin main

# 3. Actualizar aplicación
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# 4. Verificar estado
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs web
```

### Monitoreo de Producción
```bash
# Chequeo rápido de salud
docker-compose -f docker-compose.prod.yml ps

# Ver logs recientes
docker-compose -f docker-compose.prod.yml logs --tail=20

# Ver logs específicos del servicio web
docker-compose -f docker-compose.prod.yml logs -f web

# Crear backup de BD
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres gastos_hormiga_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Solución de Problemas
```bash
# Desarrollo: Reiniciar todo limpio
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Producción: Revisar problemas
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml ps

# Limpiar recursos Docker
docker system prune -f
```

## Configuración Optimizada

Esta configuración incluye:
- Django como framework web principal
- PostgreSQL como base de datos
- Nginx para producción
- Docker Compose para gestión de servicios
- n8n para automatizaciones

### Servicios Opcionales Futuros
Si necesitas agregar más funcionalidades:
- Cache (Redis)
- Tareas asíncronas (Celery)
- Búsquedas complejas (Elasticsearch)
- Monitoreo (Prometheus)

Los archivos docker-compose incluyen comentarios con configuraciones opcionales. 