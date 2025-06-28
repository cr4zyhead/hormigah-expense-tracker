"""
Utilidades para el dashboard y cálculo de métricas

Este módulo contiene toda la lógica relacionada con:
- Cálculo de períodos y fechas
- Métricas del dashboard
- Context completo del dashboard
"""

from datetime import datetime, timedelta
from django.db.models import Sum
from ..models import Expense, Budget


def get_period_dates(period):
    """
    Calcula las fechas de inicio, fin y etiqueta según el período seleccionado
    
    Args:
        period (str): Período seleccionado ('current_month', 'last_month', etc.)
    
    Returns:
        tuple: (start_date, end_date, period_label)
    """
    today = datetime.now().date()
    
    if period == 'current_month':
        start_date = today.replace(day=1)
        next_month = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)
        end_date = next_month - timedelta(days=1)
        period_label = f"Este mes ({start_date.strftime('%B %Y').title()})"
        
    elif period == 'last_month':
        first_day_current = today.replace(day=1)
        end_date = first_day_current - timedelta(days=1)
        start_date = end_date.replace(day=1)
        period_label = f"Mes pasado ({start_date.strftime('%B %Y').title()})"
        
    elif period == 'last_7_days':
        start_date = today - timedelta(days=7)
        end_date = today
        period_label = f"Últimos 7 días"
        
    elif period == 'last_30_days':
        start_date = today - timedelta(days=30)
        end_date = today
        period_label = f"Últimos 30 días"
        
    elif period == 'current_year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
        period_label = f"Este año ({today.year})"
    
    else:  # Default: current_month
        start_date = today.replace(day=1)
        next_month = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)
        end_date = next_month - timedelta(days=1)
        period_label = f"Este mes"
    
    return start_date, end_date, period_label


def calculate_dashboard_metrics(user, start_date, end_date):
    """
    Calcula todas las métricas del dashboard para el período especificado
    
    Args:
        user: Usuario actual
        start_date: Fecha de inicio del período
        end_date: Fecha de fin del período
    
    Returns:
        dict: Diccionario con todas las métricas calculadas
    """
    # Filtrar gastos por el período seleccionado
    period_expenses = Expense.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Calcular métricas básicas del período
    period_total = period_expenses.aggregate(total=Sum('amount'))['total'] or 0
    period_expenses_count = period_expenses.count()
    
    # Calcular promedio diario
    period_days = (end_date - start_date).days + 1
    period_avg_daily = period_total / period_days if period_days > 0 else 0
    
    # Gastos recientes del usuario actual (independiente del período)
    recent_expenses = Expense.objects.filter(user=user).order_by('-date')[:10]
    
    # Gastos por categoría en el período seleccionado
    categories_summary = period_expenses.values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    return {
        'period_total': period_total,
        'period_expenses_count': period_expenses_count,
        'period_avg_daily': period_avg_daily,
        'recent_expenses': recent_expenses,
        'categories_summary': categories_summary,
        # Para compatibilidad con template existente
        'monthly_total': period_total,
        'monthly_expenses_count': period_expenses_count,
        'avg_daily_expense': period_avg_daily,
    }


def get_dashboard_context(user, period):
    """
    Función principal que combina todas las métricas del dashboard
    
    Args:
        user: Usuario actual
        period: Período seleccionado
    
    Returns:
        dict: Context completo para el template del dashboard
    """
    # Importar aquí para evitar imports circulares
    from .util_chart_data import prepare_chart_data
    
    # Obtener fechas del período
    start_date, end_date, period_label = get_period_dates(period)
    
    # Calcular métricas
    metrics = calculate_dashboard_metrics(user, start_date, end_date)
    
    # Filtrar gastos del período para los gráficos
    period_expenses = Expense.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    )
    
    # Preparar datos de gráficos
    chart_data = prepare_chart_data(metrics['categories_summary'], period_expenses)
    
    # Combinar todo el context
    context = {
        **metrics,
        **chart_data,
        'period_label': period_label,
        'selected_period': period,
    }
    
    # Añadir información de presupuesto
    budget_info = get_budget_info(user, metrics['period_total'])
    context.update(budget_info)
    
    return context


def get_budget_info(user, current_month_total):
    """
    Obtiene información del presupuesto del usuario de forma sencilla
    """
    try:
        budget = Budget.objects.get(user=user)
        
        # Calcular datos básicos
        percentage_used = budget.get_percentage_used(current_month_total)
        remaining_amount = budget.get_remaining_amount(current_month_total)
        status = budget.get_status_for_amount(current_month_total)
        
        # Determinar color y mensaje según el estado
        if status == 'safe':
            color_class = 'text-green-600 bg-green-50 border-green-200'
            icon = '✅'
            message = f'¡Vas bien! Te quedan €{remaining_amount:.0f}'
        elif status == 'warning':
            color_class = 'text-yellow-600 bg-yellow-50 border-yellow-200'
            icon = '⚠️'
            message = f'¡Cuidado! Solo te quedan €{remaining_amount:.0f}'
        elif status == 'critical':
            color_class = 'text-red-600 bg-red-50 border-red-200'
            icon = '🚨'
            message = f'¡Límite casi alcanzado! Solo €{remaining_amount:.0f} restantes'
        else:  # exceeded
            color_class = 'text-red-600 bg-red-50 border-red-200'
            icon = '🛑'
            excess = current_month_total - budget.monthly_limit
            message = f'¡Límite excedido! Has gastado €{excess:.0f} de más'
        
        return {
            'has_budget': True,
            'budget': budget,
            'budget_percentage_used': percentage_used,
            'budget_remaining': remaining_amount,
            'budget_status': status,
            'budget_color_class': color_class,
            'budget_icon': icon,
            'budget_message': message,
        }
        
    except Budget.DoesNotExist:
        return {
            'has_budget': False,
            'budget': None,
        } 