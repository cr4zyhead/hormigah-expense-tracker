#!/bin/bash

# Script para facilitar el desarrollo con Docker
# Uso: ./scripts/docker-dev.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_message() {
    echo -e "${GREEN}🐳 [DOCKER-DEV]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  [WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}❌ [ERROR]${NC} $1"
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

# Función principal
main() {
    check_dependencies
    
    case ${1:-help} in
        "build")
            print_message "Construyendo imágenes de Docker..."
            docker-compose build --no-cache
            ;;
        "up")
            print_message "Iniciando servicios de desarrollo..."
            docker-compose up -d
            print_message "Servicios iniciados. La aplicación estará disponible en http://localhost:8000"
            ;;
        "down")
            print_message "Deteniendo servicios..."
            docker-compose down
            ;;
        "restart")
            print_message "Reiniciando servicios..."
            docker-compose restart
            ;;
        "logs")
            print_message "Mostrando logs..."
            docker-compose logs -f ${2:-web}
            ;;
        "shell")
            print_message "Abriendo shell en el contenedor web..."
            docker-compose exec web python manage.py shell
            ;;
        "bash")
            print_message "Abriendo bash en el contenedor web..."
            docker-compose exec web bash
            ;;
        "migrate")
            print_message "Ejecutando migraciones..."
            docker-compose exec web python manage.py migrate
            ;;
        "makemigrations")
            print_message "Creando migraciones..."
            docker-compose exec web python manage.py makemigrations
            ;;
        "collectstatic")
            print_message "Recopilando archivos estáticos..."
            docker-compose exec web python manage.py collectstatic --noinput
            ;;
        "createsuperuser")
            print_message "Creando superusuario..."
            docker-compose exec web python manage.py createsuperuser
            ;;
        "test")
            print_message "Ejecutando tests..."
            docker-compose exec web python manage.py test ${2:-}
            ;;
        "reset")
            print_warning "Esto eliminará todos los volúmenes de datos. ¿Continuar? (y/N)"
            read -r response
            if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
                print_message "Eliminando contenedores y volúmenes..."
                docker-compose down -v
                docker-compose up -d
            else
                print_message "Operación cancelada"
            fi
            ;;
        "clean")
            print_message "Limpiando imágenes y volúmenes no utilizados..."
            docker system prune -f
            ;;
        "help"|*)
            echo "🐳 Script de desarrollo con Docker"
            echo ""
            echo "Uso: $0 [comando]"
            echo ""
            echo "Comandos disponibles:"
            echo "  build          - Construir imágenes"
            echo "  up             - Iniciar servicios"
            echo "  down           - Detener servicios"
            echo "  restart        - Reiniciar servicios"
            echo "  logs [servicio]- Ver logs (por defecto: web)"
            echo "  shell          - Abrir shell de Django"
            echo "  bash           - Abrir bash en contenedor"
            echo "  migrate        - Ejecutar migraciones"
            echo "  makemigrations - Crear migraciones"
            echo "  collectstatic  - Recopilar archivos estáticos"
            echo "  createsuperuser- Crear superusuario"
            echo "  test [app]     - Ejecutar tests"
            echo "  reset          - Reiniciar con datos limpios"
            echo "  clean          - Limpiar sistema Docker"
            echo "  help           - Mostrar esta ayuda"
            ;;
    esac
}

main "$@" 