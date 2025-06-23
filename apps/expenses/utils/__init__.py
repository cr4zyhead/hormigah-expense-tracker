"""
Utils modularizados para la aplicación expenses

Este paquete contiene utilidades organizadas por responsabilidad:
- util_dashboard.py: Lógica del dashboard y métricas
- util_chart_data.py: Preparación de datos para gráficos 
- util_expense_list.py: Filtros y listado de gastos
- util_crud_operations.py: Operaciones CRUD con HTMX

Uso recomendado con imports específicos:
    from apps.expenses.utils.util_dashboard import calculate_dashboard_metrics
    from apps.expenses.utils.util_crud_operations import handle_expense_creation
    from apps.expenses.utils.util_expense_list import get_expense_list_context
    from apps.expenses.utils.util_chart_data import prepare_chart_data
    
¿Por qué imports específicos?
- Más claro y explícito
- Mejor para IDEs y autocompletado
- Evita imports circulares
- Más fácil de mantener y depurar
"""