/**
 * HORMIGAH - Sistema de Filtros Avanzados
 * Maneja la funcionalidad de filtros para gastos
 */

class ExpenseFilters {
    constructor() {
        this.form = document.querySelector('#filter-form');
        this.periodSelect = document.querySelector('#id_period');
        this.customDatesDiv = document.querySelector('#custom-dates');
        this.resetButton = document.querySelector('#reset-filters');
        this.filterStats = document.querySelector('#filter-stats');
        
        this.init();
    }

    init() {
        if (!this.form) return;
        
        this.bindEvents();
        this.updateCustomDatesVisibility();
        this.updateFilterStats();
    }

    bindEvents() {
        // Mostrar/ocultar fechas personalizadas
        if (this.periodSelect) {
            this.periodSelect.addEventListener('change', () => {
                this.updateCustomDatesVisibility();
            });
        }

        // Reset de filtros
        if (this.resetButton) {
            this.resetButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.resetFilters();
            });
        }

        // Auto-submit del formulario cuando cambian los filtros
        const filterInputs = this.form.querySelectorAll('select, input[type="date"], input[type="number"]');
        filterInputs.forEach(input => {
            input.addEventListener('change', () => {
                // Pequeño delay para mejorar UX
                setTimeout(() => {
                    this.submitFilters();
                }, 300);
            });
        });
    }

    updateCustomDatesVisibility() {
        if (!this.periodSelect || !this.customDatesDiv) return;
        
        const selectedPeriod = this.periodSelect.value;
        
        if (selectedPeriod === 'custom') {
            this.customDatesDiv.style.display = 'block';
            this.customDatesDiv.classList.add('animate-fadeIn');
        } else {
            this.customDatesDiv.style.display = 'none';
            this.customDatesDiv.classList.remove('animate-fadeIn');
            
            // Limpiar fechas personalizadas
            const dateInputs = this.customDatesDiv.querySelectorAll('input[type="date"]');
            dateInputs.forEach(input => input.value = '');
        }
    }

    resetFilters() {
        // Limpiar todos los campos del formulario
        const inputs = this.form.querySelectorAll('select, input[type="date"], input[type="number"]');
        inputs.forEach(input => {
            if (input.type === 'select-one') {
                input.selectedIndex = 0;
            } else {
                input.value = '';
            }
        });

        // Ocultar fechas personalizadas
        this.updateCustomDatesVisibility();

        // Enviar formulario para mostrar todos los gastos
        this.submitFilters();
    }

    submitFilters() {
        // Mostrar indicador de carga
        this.showLoadingIndicator();
        
        // Enviar formulario
        this.form.submit();
    }

    showLoadingIndicator() {
        // Crear o mostrar indicador de carga
        let loader = document.querySelector('#filter-loader');
        if (!loader) {
            loader = document.createElement('div');
            loader.id = 'filter-loader';
            loader.className = 'fixed top-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
            loader.innerHTML = `
                <div class="flex items-center space-x-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Filtrando gastos...</span>
                </div>
            `;
            document.body.appendChild(loader);
        } else {
            loader.style.display = 'block';
        }

        // Ocultar después de 3 segundos
        setTimeout(() => {
            if (loader) {
                loader.style.display = 'none';
            }
        }, 3000);
    }

    updateFilterStats() {
        // Esta función se puede expandir para mostrar estadísticas en tiempo real
        if (!this.filterStats) return;
        
        const activeFilters = this.getActiveFilters();
        const filterCount = Object.keys(activeFilters).length;
        
        if (filterCount > 0) {
            this.filterStats.innerHTML = `
                <div class="text-sm text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                    ${filterCount} filtro${filterCount > 1 ? 's' : ''} activo${filterCount > 1 ? 's' : ''}
                </div>
            `;
        } else {
            this.filterStats.innerHTML = '';
        }
    }

    getActiveFilters() {
        const activeFilters = {};
        const inputs = this.form.querySelectorAll('select, input[type="date"], input[type="number"]');
        
        inputs.forEach(input => {
            if (input.value && input.value !== '') {
                activeFilters[input.name] = input.value;
            }
        });
        
        return activeFilters;
    }
}

// Utilidades adicionales
class FilterUtils {
    static formatCurrency(amount) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'EUR'
        }).format(amount);
    }

    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    static showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 
            'bg-blue-500'
        } text-white`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new ExpenseFilters();
});

// Exportar para uso en otros scripts si es necesario
window.ExpenseFilters = ExpenseFilters;
window.FilterUtils = FilterUtils; 