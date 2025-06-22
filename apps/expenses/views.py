from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
import json
from .models import Expense, Category
from .forms import ExpenseForm, ExpenseFilterForm
from .utils import get_dashboard_context


@login_required
def dashboard(request):
    """
    Vista del dashboard refactorizada - limpia y enfocada
    Maneja filtros de período con HTMX
    """
    # Obtener el período seleccionado del filtro
    period = request.GET.get('period', 'current_month')
    
    # Obtener todo el contexto del dashboard usando las funciones auxiliares
    context = get_dashboard_context(request.user, period)
    
    # Si es una petición HTMX, devolver solo las métricas
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/dashboard_metrics.html', context)
    
    return render(request, 'expenses/dashboard.html', context)


@login_required
def expense_list(request):
    """
    Vista profesional que maneja tanto peticiones normales como HTMX
    Devuelve página completa o contenido parcial según el tipo de petición
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
    
    # Context común para ambos tipos de respuesta
    context = {
        'expenses': expenses,
        'total_filtered': total_filtered,
        'count_filtered': count_filtered,
        'has_filters': has_filters,
        'active_period_info': active_period_info,
        'period_dates': period_dates,
    }
    
    # ¿Es una petición HTMX? Devolver solo contenido parcial
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/expense_list_content.html', context)
    
    # Petición normal: devolver página completa con formulario
    context['filter_form'] = filter_form
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



