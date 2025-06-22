from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
import json
from .models import Expense, Category
from .forms import ExpenseForm, ExpenseFilterForm


@login_required
def dashboard(request):
    """
    Vista principal del dashboard que muestra resumen de gastos con gráficas
    """
    # Gastos recientes del usuario actual
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:10]
    
    # Fechas para filtros
    current_month = datetime.now().month
    current_year = datetime.now().year
    last_30_days = datetime.now().date() - timedelta(days=30)
    
    # Total de gastos del mes actual
    monthly_total = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Gastos por categoría últimos 30 días (para tabla y gráfica dona)
    categories_summary = Expense.objects.filter(
        user=request.user,
        date__gte=last_30_days
    ).values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Datos para gráfico de dona (JSON)
    chart_categories = list(categories_summary.values_list('category__name', flat=True))
    chart_amounts = list(categories_summary.values_list('total', flat=True))
    chart_colors = list(categories_summary.values_list('category__color', flat=True))
    
    # Gastos por día en los últimos 30 días (para gráfico de líneas)
    daily_expenses = Expense.objects.filter(
        user=request.user,
        date__gte=last_30_days
    ).annotate(
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
    
    # Estadísticas adicionales
    # Total de gastos del mes actual (para consistencia con monthly_total)
    monthly_expenses_count = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).count()
    
    # Promedio diario de los últimos 30 días
    avg_daily_expense = Expense.objects.filter(
        user=request.user,
        date__gte=last_30_days
    ).aggregate(avg=Sum('amount'))['avg'] or 0
    if avg_daily_expense:
        avg_daily_expense = avg_daily_expense / 30
    
    context = {
        'recent_expenses': recent_expenses,
        'monthly_total': monthly_total,
        'categories_summary': categories_summary,
        'monthly_expenses_count': monthly_expenses_count,
        'avg_daily_expense': avg_daily_expense,
        
        # Datos para Chart.js (convertidos a JSON)
        'chart_categories_json': json.dumps(chart_categories),
        'chart_amounts_json': json.dumps([float(amount) for amount in chart_amounts]),
        'chart_colors_json': json.dumps(chart_colors),
        'chart_dates_json': json.dumps(chart_dates),
        'chart_daily_amounts_json': json.dumps(chart_daily_amounts),
    }
    
    return render(request, 'expenses/dashboard.html', context)


@login_required
def expense_list(request):
    """
    Vista que muestra la lista completa de gastos del usuario con filtros avanzados
    """
    # Obtener todos los gastos del usuario
    expenses = Expense.objects.filter(user=request.user)
    
    # Inicializar el formulario de filtros
    filter_form = ExpenseFilterForm(request.GET or None)
    
    # Variables para mostrar información del período activo
    active_period_info = None
    period_dates = None
    
    # Aplicar filtros si el formulario es válido
    if filter_form.is_valid():
        # Filtro por período predefinido
        period = filter_form.cleaned_data.get('period')
        if period:
            today = datetime.now().date()
            
            if period == 'current_month':
                start_date = today.replace(day=1)
                next_month = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)
                end_date = next_month - timedelta(days=1)
                expenses = expenses.filter(date__gte=start_date, date__lte=end_date)
                active_period_info = f"Gastos de {start_date.strftime('%B %Y').title()}"
                period_dates = (start_date, end_date)
                
            elif period == 'last_month':
                first_day_current = today.replace(day=1)
                last_day_previous = first_day_current - timedelta(days=1)
                first_day_previous = last_day_previous.replace(day=1)
                expenses = expenses.filter(date__gte=first_day_previous, date__lte=last_day_previous)
                active_period_info = f"Gastos de {first_day_previous.strftime('%B %Y').title()}"
                period_dates = (first_day_previous, last_day_previous)
                
            elif period == 'last_7_days':
                start_date = today - timedelta(days=7)
                expenses = expenses.filter(date__gte=start_date, date__lte=today)
                active_period_info = f"Gastos de los últimos 7 días ({start_date.strftime('%d/%m')} - {today.strftime('%d/%m')})"
                period_dates = (start_date, today)
                
            elif period == 'last_30_days':
                start_date = today - timedelta(days=30)
                expenses = expenses.filter(date__gte=start_date, date__lte=today)
                active_period_info = f"Gastos de los últimos 30 días ({start_date.strftime('%d/%m')} - {today.strftime('%d/%m')})"
                period_dates = (start_date, today)
        
        # Filtro por categoría
        category = filter_form.cleaned_data.get('category')
        if category:
            expenses = expenses.filter(category=category)
        
        # Filtro por fecha desde (solo si no hay período predefinido)
        if not period:
            date_from = filter_form.cleaned_data.get('date_from')
            if date_from:
                expenses = expenses.filter(date__gte=date_from)
        
        # Filtro por fecha hasta (solo si no hay período predefinido)
        if not period:
            date_to = filter_form.cleaned_data.get('date_to')
            if date_to:
                expenses = expenses.filter(date__lte=date_to)
        
        # Filtro por monto mínimo
        min_amount = filter_form.cleaned_data.get('min_amount')
        if min_amount:
            expenses = expenses.filter(amount__gte=min_amount)
        
        # Filtro por monto máximo
        max_amount = filter_form.cleaned_data.get('max_amount')
        if max_amount:
            expenses = expenses.filter(amount__lte=max_amount)
    
    # Ordenar por fecha (más recientes primero)
    expenses = expenses.order_by('-date')
    
    # Calcular estadísticas de los gastos filtrados
    total_filtered = expenses.aggregate(total=Sum('amount'))['total'] or 0
    count_filtered = expenses.count()
    
    # Detectar filtros activos
    has_filters = False
    if filter_form.is_valid():
        has_filters = any([
            filter_form.cleaned_data.get('period'),
            filter_form.cleaned_data.get('category'),
            filter_form.cleaned_data.get('date_from'),
            filter_form.cleaned_data.get('date_to'),
            filter_form.cleaned_data.get('min_amount'),
            filter_form.cleaned_data.get('max_amount'),
        ])
    
    context = {
        'expenses': expenses,
        'filter_form': filter_form,
        'total_filtered': total_filtered,
        'count_filtered': count_filtered,
        'has_filters': has_filters,
        'active_period_info': active_period_info,
        'period_dates': period_dates,
    }
    
    return render(request, 'expenses/expense_list.html', context)


@login_required
def add_expense(request):
    """
    Vista para agregar un nuevo gasto
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, '¡Gasto agregado exitosamente!')
            return redirect('expenses:dashboard')
    else:
        form = ExpenseForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'expenses/add_expense.html', context)


@login_required
def expense_list_htmx(request):
    """
    Vista HTMX que devuelve solo la parte actualizable de la lista de gastos
    Esta vista es llamada por HTMX para actualizar la lista sin recargar toda la página
    """
    # Reutilizamos la misma lógica de expense_list
    expenses = Expense.objects.filter(user=request.user)
    
    # Inicializar el formulario de filtros
    filter_form = ExpenseFilterForm(request.GET or None)
    
    # Variables para mostrar información del período activo
    active_period_info = None
    period_dates = None
    
    # Aplicar filtros si el formulario es válido
    if filter_form.is_valid():
        # Filtro por período predefinido
        period = filter_form.cleaned_data.get('period')
        if period:
            today = datetime.now().date()
            
            if period == 'current_month':
                start_date = today.replace(day=1)
                next_month = start_date.replace(month=start_date.month + 1) if start_date.month < 12 else start_date.replace(year=start_date.year + 1, month=1)
                end_date = next_month - timedelta(days=1)
                expenses = expenses.filter(date__gte=start_date, date__lte=end_date)
                active_period_info = f"Gastos de {start_date.strftime('%B %Y').title()}"
                period_dates = (start_date, end_date)
                
            elif period == 'last_month':
                first_day_current = today.replace(day=1)
                last_day_previous = first_day_current - timedelta(days=1)
                first_day_previous = last_day_previous.replace(day=1)
                expenses = expenses.filter(date__gte=first_day_previous, date__lte=last_day_previous)
                active_period_info = f"Gastos de {first_day_previous.strftime('%B %Y').title()}"
                period_dates = (first_day_previous, last_day_previous)
                
            elif period == 'last_7_days':
                start_date = today - timedelta(days=7)
                expenses = expenses.filter(date__gte=start_date, date__lte=today)
                active_period_info = f"Gastos de los últimos 7 días ({start_date.strftime('%d/%m')} - {today.strftime('%d/%m')})"
                period_dates = (start_date, today)
                
            elif period == 'last_30_days':
                start_date = today - timedelta(days=30)
                expenses = expenses.filter(date__gte=start_date, date__lte=today)
                active_period_info = f"Gastos de los últimos 30 días ({start_date.strftime('%d/%m')} - {today.strftime('%d/%m')})"
                period_dates = (start_date, today)
        
        # Filtro por categoría
        category = filter_form.cleaned_data.get('category')
        if category:
            expenses = expenses.filter(category=category)
        
        # Filtro por fecha desde (solo si no hay período predefinido)
        if not period:
            date_from = filter_form.cleaned_data.get('date_from')
            if date_from:
                expenses = expenses.filter(date__gte=date_from)
        
        # Filtro por fecha hasta (solo si no hay período predefinido)
        if not period:
            date_to = filter_form.cleaned_data.get('date_to')
            if date_to:
                expenses = expenses.filter(date__lte=date_to)
        
        # Filtro por monto mínimo
        min_amount = filter_form.cleaned_data.get('min_amount')
        if min_amount:
            expenses = expenses.filter(amount__gte=min_amount)
        
        # Filtro por monto máximo
        max_amount = filter_form.cleaned_data.get('max_amount')
        if max_amount:
            expenses = expenses.filter(amount__lte=max_amount)
    
    # Ordenar por fecha (más recientes primero)
    expenses = expenses.order_by('-date')
    
    # Calcular estadísticas de los gastos filtrados
    total_filtered = expenses.aggregate(total=Sum('amount'))['total'] or 0
    count_filtered = expenses.count()
    
    # Detectar filtros activos
    has_filters = False
    if filter_form.is_valid():
        has_filters = any([
            filter_form.cleaned_data.get('period'),
            filter_form.cleaned_data.get('category'),
            filter_form.cleaned_data.get('date_from'),
            filter_form.cleaned_data.get('date_to'),
            filter_form.cleaned_data.get('min_amount'),
            filter_form.cleaned_data.get('max_amount'),
        ])
    
    context = {
        'expenses': expenses,
        'total_filtered': total_filtered,
        'count_filtered': count_filtered,
        'has_filters': has_filters,
        'active_period_info': active_period_info,
        'period_dates': period_dates,
    }
    
    # Devolver solo el template parcial para HTMX
    return render(request, 'expenses/partials/expense_list_content.html', context)
