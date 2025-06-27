#!/bin/bash

# Script para manejar el entorno de producción con Docker
# Uso: ./scripts/docker-prod.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_message() {
    echo -e "${GREEN}[DOCKER-PROD]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Verificar que docker y docker-compose estén instalados
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado"
        exit 1
    fi
}

# Verificar que existe el archivo .env.production
check_env_file() {
    if [ ! -f ".env.production" ]; then
        print_error "Archivo .env.production no encontrado"
        print_info "Copia .env.example a .env.production y configura las variables"
        exit 1
    fi
}

# Función principal
main() {
    check_dependencies
    
    case ${1:-help} in
        "build")
            print_message "Construyendo imágenes para producción..."
            docker-compose -f docker-compose.prod.yml build --no-cache
            ;;
        "up")
            check_env_file
            print_message "Iniciando servicios de producción..."
            docker-compose -f docker-compose.prod.yml up -d
            print_message "Servicios iniciados. La aplicación estará disponible en http://localhost"
            ;;
        "down")
            print_message "Deteniendo servicios de producción..."
            docker-compose -f docker-compose.prod.yml down
            ;;
        "restart")
            print_message "Reiniciando servicios de producción..."
            docker-compose -f docker-compose.prod.yml restart
            ;;
        "logs")
            print_message "Mostrando logs de producción..."
            docker-compose -f docker-compose.prod.yml logs -f ${2:-web}
            ;;
        "migrate")
            print_message "Ejecutando migraciones en producción..."
            docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
            ;;
        "collectstatic")
            print_message "Recopilando archivos estáticos en producción..."
            docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
            ;;
        "backup")
            print_message "Creando backup de la base de datos..."
            timestamp=$(date +%Y%m%d_%H%M%S)
            docker-compose -f docker-compose.prod.yml exec db pg_dump -U ${DB_USER:-postgres} ${DB_NAME:-gastos_hormiga_prod} > backup_${timestamp}.sql
            print_message "Backup creado: backup_${timestamp}.sql"
            ;;
        "restore")
            if [ -z "$2" ]; then
                print_error "Especifica el archivo de backup: $0 restore backup_file.sql"
                exit 1
            fi
            print_warning "Esto restaurará la base de datos desde $2. ¿Continuar? (y/N)"
            read -r response
            if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                print_message "Restaurando base de datos desde $2..."
                docker-compose -f docker-compose.prod.yml exec -T db psql -U ${DB_USER:-postgres} -d ${DB_NAME:-gastos_hormiga_prod} < "$2"
                print_message "Base de datos restaurada"
            else
                print_message "Operación cancelada"
            fi
            ;;
        "update")
            print_message "Actualizando aplicación en producción..."
            docker-compose -f docker-compose.prod.yml pull
            docker-compose -f docker-compose.prod.yml build
            docker-compose -f docker-compose.prod.yml up -d
            print_message "Aplicación actualizada"
            ;;
        "status")
            print_message "Estado de los servicios:"
            docker-compose -f docker-compose.prod.yml ps
            ;;
        "clean")
            print_warning "Esto eliminará imágenes no utilizadas. ¿Continuar? (y/N)"
            read -r response
            if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                print_message "Limpiando sistema Docker..."
                docker system prune -f
            else
                print_message "Operación cancelada"
            fi
            ;;
        "help"|*)
            echo "Script de producción con Docker"
            echo ""
            echo "Uso: $0 [comando]"
            echo ""
            echo "Comandos disponibles:"
            echo "  build           - Construir imágenes para producción"
            echo "  up              - Iniciar servicios de producción"
            echo "  down            - Detener servicios de producción"
            echo "  restart         - Reiniciar servicios"
            echo "  logs [servicio] - Ver logs (por defecto: web)"
            echo "  migrate         - Ejecutar migraciones"
            echo "  collectstatic   - Recopilar archivos estáticos"
            echo "  backup          - Crear backup de la base de datos"
            echo "  restore <file>  - Restaurar base de datos desde backup"
            echo "  update          - Actualizar aplicación"
            echo "  status          - Ver estado de servicios"
            echo "  clean           - Limpiar sistema Docker"
            echo "  help            - Mostrar esta ayuda"
            ;;
    esac
}

main "$@" 