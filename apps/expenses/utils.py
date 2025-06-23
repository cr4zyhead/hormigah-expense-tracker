from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
import json
from .models import Expense
from .forms import ExpenseFilterForm


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


def apply_expense_filters(expenses, filter_form):
    """
    Aplica todos los filtros a un QuerySet de gastos
    
    Args:
        expenses: QuerySet base de gastos
        filter_form: Formulario de filtros validado
    
    Returns:
        tuple: (expenses_filtered, active_period_info, period_dates)
    """
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


def get_expense_for_user(expense_id, user):
    """
    Obtiene un gasto específico verificando que pertenece al usuario
    
    Args:
        expense_id: ID del gasto
        user: Usuario actual
    
    Returns:
        Expense: Objeto del gasto o None si no existe/no pertenece al usuario
    
    Raises:
        Expense.DoesNotExist: Si el gasto no existe o no pertenece al usuario
    """
    try:
        return Expense.objects.get(id=expense_id, user=user)
    except Expense.DoesNotExist:
        raise Expense.DoesNotExist("El gasto no existe o no tienes permisos para acceder a él")


def handle_expense_form_update(expense, form_data):
    """
    Maneja la actualización de un gasto con los datos del formulario
    
    Args:
        expense: Instancia del gasto a actualizar
        form_data: Datos POST del formulario
    
    Returns:
        tuple: (updated_expense, form, is_valid)
    """
    from .forms import ExpenseForm
    
    form = ExpenseForm(form_data, instance=expense)
    
    if form.is_valid():
        updated_expense = form.save()
        return updated_expense, form, True
    
    return expense, form, False


def build_expense_edit_context(user, expense, form, request_params):
    """
    Construye el contexto para mostrar después de una edición exitosa
    
    Args:
        user: Usuario actual
        expense: Gasto actualizado
        form: Formulario usado
        request_params: Parámetros GET de la petición
    
    Returns:
        dict: Context actualizado con mensaje de éxito
    """
    # Obtener contexto actualizado de la lista
    context = get_expense_list_context(user, request_params)
    
    # Agregar información específica de la edición
    context.update({
        'edit_success': True,
        'expense_data': {
            'amount': expense.amount,
            'category_name': expense.category.name,
            'description': expense.description or 'Sin descripción',
            'date': expense.date
        },
        'edit_message': 'Gasto actualizado exitosamente'
    })
    
    return context


def handle_expense_error_response(request, error_message):
    """
    Maneja respuestas de error de forma consistente
    
    Args:
        request: Objeto request de Django
        error_message: Mensaje de error a mostrar
    
    Returns:
        HttpResponse: Respuesta apropiada según el tipo de petición
    """
    from django.shortcuts import render
    from django.contrib import messages
    from django.shortcuts import redirect
    
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/delete_error.html', {
            'error': error_message
        })
    
    messages.error(request, error_message)
    return redirect('expenses:expense_list')


def create_htmx_edit_response(request, context):
    """
    Crea respuesta HTMX para edición exitosa con trigger para cerrar modal
    
    Args:
        request: Objeto request de Django
        context: Context para el template
    
    Returns:
        HttpResponse: Respuesta con header HX-Trigger-After-Swap
    """
    from django.shortcuts import render
    
    response = render(request, 'expenses/partials/expense_list_content.html', context)
    response['HX-Trigger-After-Swap'] = 'closeEditModal'
    return response


def handle_expense_creation(form_data, user):
    """
    Maneja la creación de un nuevo gasto con los datos del formulario
    
    Args:
        form_data: Datos POST del formulario
        user: Usuario actual
    
    Returns:
        tuple: (expense, form, is_valid)
    """
    from .forms import ExpenseForm
    
    form = ExpenseForm(form_data)
    
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = user
        expense.save()
        return expense, form, True
    
    return None, form, False


def create_htmx_add_response(request, expense):
    """
    Crea respuesta HTMX para creación exitosa con trigger para cerrar modal
    
    Args:
        request: Objeto request de Django
        expense: Gasto creado exitosamente
    
    Returns:
        HttpResponse: Respuesta con mensaje de éxito
    """
    from django.shortcuts import render
    
    response = render(request, 'expenses/partials/expense_success.html', {
        'expense': expense,
        'message': '¡Gasto agregado exitosamente!'
    })
    return response


def build_add_expense_context(form=None):
    """
    Construye el contexto para el formulario de agregar gasto
    
    Args:
        form: Formulario (nuevo o con errores)
    
    Returns:
        dict: Context para el template
    """
    from .forms import ExpenseForm
    
    if form is None:
        form = ExpenseForm()
    
    return {
        'form': form
    } 