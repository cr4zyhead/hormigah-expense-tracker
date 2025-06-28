# Gastos Hormiga - Configuración Docker

## Introducción

Esta aplicación Django ha sido configurada para ejecutarse con Docker y PostgreSQL. Incluye configuraciones separadas para desarrollo y producción.

## Scripts Helper

> **Opcional**: Para facilitar el trabajo con Docker, la aplicación incluye scripts que simplifican las operaciones más comunes:

- **`scripts/docker-dev.sh`** - Para desarrollo local
- **`scripts/docker-prod.sh`** - Para producción

Estos scripts son una **alternativa opcional** a los comandos estándar de Docker Compose. Puedes elegir usar cualquiera de los dos enfoques según tu preferencia.

### Comandos Disponibles

#### Development (`docker-dev.sh`)
```bash
./scripts/docker-dev.sh build          # Construir imágenes
./scripts/docker-dev.sh up             # Iniciar servicios
./scripts/docker-dev.sh down           # Detener servicios
./scripts/docker-dev.sh restart        # Reiniciar servicios
./scripts/docker-dev.sh logs           # Ver logs
./scripts/docker-dev.sh shell          # Django shell
./scripts/docker-dev.sh bash           # Bash en contenedor
./scripts/docker-dev.sh migrate        # Ejecutar migraciones
./scripts/docker-dev.sh makemigrations # Crear migraciones
./scripts/docker-dev.sh collectstatic  # Recopilar archivos estáticos
./scripts/docker-dev.sh createsuperuser# Crear superusuario
./scripts/docker-dev.sh test [app]     # Ejecutar tests
./scripts/docker-dev.sh reset          # Reiniciar con datos limpios
./scripts/docker-dev.sh clean          # Limpiar sistema Docker
./scripts/docker-dev.sh help           # Mostrar ayuda
```

#### Producción (`docker-prod.sh`)
```bash
./scripts/docker-prod.sh build         # Construir imágenes para producción
./scripts/docker-prod.sh up            # Iniciar servicios de producción
./scripts/docker-prod.sh down          # Detener servicios de producción
./scripts/docker-prod.sh restart       # Reiniciar servicios
./scripts/docker-prod.sh logs          # Ver logs de producción
./scripts/docker-prod.sh migrate       # Ejecutar migraciones
./scripts/docker-prod.sh collectstatic # Recopilar archivos estáticos
./scripts/docker-prod.sh backup        # Crear backup de la base de datos
./scripts/docker-prod.sh restore <file># Restaurar base de datos desde backup
./scripts/docker-prod.sh update        # Actualizar aplicación
./scripts/docker-prod.sh status        # Ver estado de servicios
./scripts/docker-prod.sh clean         # Limpiar sistema Docker
./scripts/docker-prod.sh help          # Mostrar ayuda
```

### Características de los Scripts

- **Comandos más cortos**: `./scripts/docker-dev.sh up` vs `docker-compose up -d`
- **Validaciones automáticas**: Verifican dependencias y archivos necesarios
- **Feedback visual**: Mensajes con colores para mejor experiencia de usuario
- **Gestión de errores**: Manejo inteligente de errores comunes
- **Confirmaciones de seguridad**: Para operaciones destructivas como `reset`

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

## Workflows Completos

### Desarrollo Local - Primer Setup
```bash
# 1. Configurar entorno
cp .env.example .env.local

# 2. Construir e iniciar
./scripts/docker-dev.sh build
./scripts/docker-dev.sh up

# 3. Configurar Django
./scripts/docker-dev.sh migrate
./scripts/docker-dev.sh createsuperuser

# 4. ¡Listo! Aplicación disponible en http://localhost:8000
```

### Desarrollo Local - Día a Día
```bash
# Iniciar trabajo
./scripts/docker-dev.sh up

# Crear/aplicar migraciones
./scripts/docker-dev.sh makemigrations
./scripts/docker-dev.sh migrate

# Ejecutar tests
./scripts/docker-dev.sh test

# Ver logs si hay problemas
./scripts/docker-dev.sh logs

# Terminar trabajo
./scripts/docker-dev.sh down
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
./scripts/docker-prod.sh build
./scripts/docker-prod.sh up

# 4. Verificar estado
./scripts/docker-prod.sh status
```

### Actualización en Producción
```bash
# 1. Conectar al servidor
ssh root@tu-servidor-ip
cd /ruta/a/tu/aplicacion

# 2. Actualizar código
git pull origin main

# 3. Actualizar aplicación (incluye pull, build, restart)
./scripts/docker-prod.sh update

# 4. Verificar estado
./scripts/docker-prod.sh status
./scripts/docker-prod.sh logs
```

### Monitoreo de Producción
```bash
# Chequeo rápido de salud
./scripts/docker-prod.sh status

# Ver logs recientes
./scripts/docker-prod.sh logs

# Ver logs específicos del servicio web
./scripts/docker-prod.sh logs web

# Crear backup de BD (recomendado antes de actualizaciones)
./scripts/docker-prod.sh backup
```

### Solución de Problemas con Scripts
```bash
# Desarrollo: Reiniciar todo limpio
./scripts/docker-dev.sh reset

# Producción: Revisar problemas
./scripts/docker-prod.sh logs
./scripts/docker-prod.sh status

# Ambos: Limpiar recursos Docker
./scripts/docker-dev.sh clean     # o docker-prod.sh clean
```

## Configuración Optimizada

Esta configuración incluye:
- Django como framework web principal
- PostgreSQL como base de datos
- Nginx para producción
- Docker para todos los entornos
- **Scripts helper para operaciones simplificadas**

### Servicios Opcionales Futuros
Si necesitas agregar más funcionalidades:
- Cache (Redis)
- Tareas asíncronas (Celery)
- Búsquedas complejas (Elasticsearch)
- Monitoreo (Prometheus)

Los archivos docker-compose incluyen comentarios con configuraciones opcionales. 