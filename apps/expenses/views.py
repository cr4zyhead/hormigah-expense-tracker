from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
import json
from .models import Expense, Category
from .forms import ExpenseForm


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
    
    # Gastos por categoría este mes (para tabla y gráfica dona)
    categories_summary = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
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
    total_expenses_count = Expense.objects.filter(user=request.user).count()
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
        'total_expenses_count': total_expenses_count,
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
    Vista que muestra la lista completa de gastos del usuario
    """
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'expenses': expenses,
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
