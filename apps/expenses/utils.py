from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
import json
from .models import Expense


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


def prepare_chart_data(categories_summary, period_expenses):
    """
    Prepara los datos para los gráficos Chart.js
    
    Args:
        categories_summary: QuerySet con resumen por categorías
        period_expenses: QuerySet con gastos del período
    
    Returns:
        dict: Datos preparados para Chart.js en formato JSON
    """
    # Datos para gráfico de dona (categorías)
    chart_categories = list(categories_summary.values_list('category__name', flat=True))
    chart_amounts = list(categories_summary.values_list('total', flat=True))
    chart_colors = list(categories_summary.values_list('category__color', flat=True))
    
    # Gastos por día (gráfico de líneas)
    daily_expenses = period_expenses.annotate(
        day=TruncDay('date')
    ).values('day').annotate(
        total=Sum('amount')
    ).order_by('day')
    
    # Preparar datos para gráfico de líneas
    chart_dates = []
    chart_daily_amounts = []
    for expense in daily_expenses:
        chart_dates.append(expense['day'].strftime('%Y-%m-%d'))
        chart_daily_amounts.append(float(expense['total']))
    
    return {
        'chart_categories_json': json.dumps(chart_categories),
        'chart_amounts_json': json.dumps([float(amount) for amount in chart_amounts]),
        'chart_colors_json': json.dumps(chart_colors),
        'chart_dates_json': json.dumps(chart_dates),
        'chart_daily_amounts_json': json.dumps(chart_daily_amounts),
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
    
    return context 