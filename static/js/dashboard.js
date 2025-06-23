/**
 * Dashboard JavaScript - Hormigah App
 * Maneja gráficos Chart.js y funcionalidad del dashboard
 */

// Configuración global de Chart.js
Chart.defaults.font.family = 'Nunito, system-ui, sans-serif';
Chart.defaults.color = '#6B7280';

// Event listener para auto-refresh del dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Listener para recargar página después de agregar gasto en dashboard
    document.body.addEventListener('refreshDashboard', function() {
        setTimeout(function() {
            window.location.reload();
        }, 1500); // Esperar 1.5 segundos para ver el mensaje
    });
});

/**
 * Inicializa el gráfico de dona de categorías
 * @param {Object} data - Datos para el gráfico
 */
function initCategoryChart(data) {
    const categoryCtx = document.getElementById('categoryChart');
    if (!categoryCtx) return;
    
    new Chart(categoryCtx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: data.categories,
            datasets: [{
                data: data.amounts,
                backgroundColor: data.colors,
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return context.label + ': $' + value.toLocaleString() + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Inicializa el gráfico de líneas de tendencia
 * @param {Object} data - Datos para el gráfico
 */
function initTrendChart(data) {
    const trendCtx = document.getElementById('trendChart');
    if (!trendCtx) return;
    
    new Chart(trendCtx.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Gastos Diarios',
                data: data.amounts,
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#3B82F6',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Gasto: $' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Fecha'
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Monto ($)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

/**
 * Inicializa todos los gráficos del dashboard
 * @param {Object} chartData - Todos los datos de gráficos
 */
function initDashboardCharts(chartData) {
    // Inicializar gráfico de categorías si hay datos
    if (chartData.categories && chartData.categories.length > 0) {
        initCategoryChart({
            categories: chartData.categories,
            amounts: chartData.amounts,
            colors: chartData.colors
        });
    }
    
    // Inicializar gráfico de tendencia si hay datos
    if (chartData.dates && chartData.dates.length > 0) {
        initTrendChart({
            dates: chartData.dates,
            amounts: chartData.dailyAmounts
        });
    }
} 