# Gastos Hormiga - Configuración Docker

## Introducción

Esta aplicación Django ha sido configurada para ejecutarse con Docker y PostgreSQL. Incluye configuraciones separadas para desarrollo y producción.

## Arquitectura

### Desarrollo (`docker-compose.yml`)
- **web**: Aplicación Django con hot reload
- **db**: PostgreSQL 15

### Producción (`docker-compose.prod.yml`)
- **web**: Aplicación Django con Gunicorn
- **db**: PostgreSQL 15
- **nginx**: Servidor web y proxy inverso

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
docker-compose up -d
```

### 4. Crear Superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Acceder a la Aplicación
- **Aplicación**: http://localhost:8000
- **Panel Admin**: http://localhost:8000/admin

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
└── .env.production        # Variables producción
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
```

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

## Configuración Optimizada

Esta configuración incluye:
- Django como framework web principal
- PostgreSQL como base de datos
- Nginx para producción
- Docker para todos los entornos

### Servicios Opcionales Futuros
Si necesitas agregar más funcionalidades:
- Cache (Redis)
- Tareas asíncronas (Celery)
- Búsquedas complejas (Elasticsearch)
- Monitoreo (Prometheus)

Los archivos docker-compose incluyen comentarios con configuraciones opcionales. 