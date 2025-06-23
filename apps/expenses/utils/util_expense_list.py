"""
Utilidades para manejo de listas de gastos y filtros

Este módulo contiene funciones especializadas en:
- Aplicación de filtros a gastos
- Cálculo de estadísticas de gastos
- Detección de filtros activos
- Context completo para listado de gastos
"""

from django.db.models import Sum
from ..models import Expense
from ..forms import ExpenseFilterForm


def apply_expense_filters(expenses, filter_form):
    """
    Aplica todos los filtros a un QuerySet de gastos
    
    Args:
        expenses: QuerySet base de gastos
        filter_form: Formulario de filtros validado
    
    Returns:
        tuple: (expenses_filtered, active_period_info, period_dates)
    """
    # Importar aquí para evitar imports circulares
    from .util_dashboard import get_period_dates
    
    active_period_info = None
    period_dates = None
    
    if not filter_form.is_valid():
        return expenses, active_period_info, period_dates
    
    # Filtro por período predefinido (reutilizando lógica existente)
    period = filter_form.cleaned_data.get('period')
    if period:
        start_date, end_date, period_label = get_period_dates(period)
        expenses = expenses.filter(date__gte=start_date, date__lte=end_date)
        active_period_info = period_label
        period_dates = (start_date, end_date)
    
    # Filtro por categoría
    category = filter_form.cleaned_data.get('category')
    if category:
        expenses = expenses.filter(category=category)
    
    # Filtros por fecha personalizada (solo si no hay período predefinido)
    if not period:
        date_from = filter_form.cleaned_data.get('date_from')
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        
        date_to = filter_form.cleaned_data.get('date_to')
        if date_to:
            expenses = expenses.filter(date__lte=date_to)
    
    # Filtros por monto
    min_amount = filter_form.cleaned_data.get('min_amount')
    if min_amount:
        expenses = expenses.filter(amount__gte=min_amount)
    
    max_amount = filter_form.cleaned_data.get('max_amount')
    if max_amount:
        expenses = expenses.filter(amount__lte=max_amount)
    
    return expenses, active_period_info, period_dates


def calculate_expense_statistics(expenses):
    """
    Calcula estadísticas de un QuerySet de gastos
    
    Args:
        expenses: QuerySet de gastos
    
    Returns:
        dict: Estadísticas calculadas
    """
    total_filtered = expenses.aggregate(total=Sum('amount'))['total'] or 0
    count_filtered = expenses.count()
    
    return {
        'total_filtered': total_filtered,
        'count_filtered': count_filtered,
    }


def detect_active_filters(filter_form):
    """
    Detecta si hay filtros activos en el formulario
    
    Args:
        filter_form: Formulario de filtros validado
    
    Returns:
        bool: True si hay filtros activos
    """
    if not filter_form.is_valid():
        return False
    
    return any([
        filter_form.cleaned_data.get('period'),
        filter_form.cleaned_data.get('category'),
        filter_form.cleaned_data.get('date_from'),
        filter_form.cleaned_data.get('date_to'),
        filter_form.cleaned_data.get('min_amount'),
        filter_form.cleaned_data.get('max_amount'),
    ])


def get_expense_list_context(user, request_params):
    """
    Función principal que genera el contexto completo para expense_list
    
    Args:
        user: Usuario actual
        request_params: Parámetros GET de la petición
    
    Returns:
        dict: Context completo para el template
    """
    # Obtener todos los gastos del usuario
    expenses = Expense.objects.filter(user=user)
    
    # Inicializar formulario de filtros
    filter_form = ExpenseFilterForm(request_params or None)
    
    # Aplicar filtros
    expenses, active_period_info, period_dates = apply_expense_filters(expenses, filter_form)
    
    # Ordenar por fecha (más recientes primero)
    expenses = expenses.order_by('-date')
    
    # Calcular estadísticas
    statistics = calculate_expense_statistics(expenses)
    
    # Detectar filtros activos
    has_filters = detect_active_filters(filter_form)
    
    # Construir contexto
    context = {
        'expenses': expenses,
        'has_filters': has_filters,
        'active_period_info': active_period_info,
        'period_dates': period_dates,
        'filter_form': filter_form,
        **statistics,  # total_filtered, count_filtered
    }
    
    return context 