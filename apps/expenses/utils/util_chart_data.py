"""
Utilidades para preparación de datos de gráficos

Este módulo contiene funciones especializadas en:
- Preparación de datos para Chart.js
- Formateo de datos para gráficos de dona
- Formateo de datos para gráficos de líneas
"""

import json
from django.db.models import Sum
from django.db.models.functions import TruncDay


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