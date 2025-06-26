#!/bin/bash

# Script de entrada para el contenedor Django
# Este script se encarga de preparar el entorno antes de ejecutar la aplicación

set -e

# Función para imprimir mensajes con formato
print_message() {
    echo "🐍 [DJANGO] $1"
}

# Esperar a que PostgreSQL esté disponible
print_message "Esperando a que PostgreSQL esté disponible..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done
print_message "PostgreSQL está disponible!"

# Ejecutar migraciones
print_message "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Recopilar archivos estáticos
print_message "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe (solo en desarrollo)
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.local" ]; then
    print_message "Creando superusuario para desarrollo..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gastoshormiga.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Superusuario ya existe')
"
fi

# Cargar datos de prueba (solo en desarrollo)
if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.local" ] && [ "$LOAD_FIXTURES" = "true" ]; then
    print_message "Cargando datos de prueba..."
    python manage.py loaddata apps/expenses/fixtures/*.json 2>/dev/null || true
fi

print_message "¡Aplicación lista!"

# Ejecutar el comando pasado como argumento
exec "$@" 