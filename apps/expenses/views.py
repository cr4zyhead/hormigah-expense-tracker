from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm


@login_required
def dashboard(request):
    """
    Vista principal del dashboard que muestra resumen de gastos
    """
    # Gastos recientes del usuario actual
    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:10]
    
    # Total de gastos del mes actual
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_total = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Gastos por categoría este mes
    categories_summary = Expense.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    ).values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    context = {
        'recent_expenses': recent_expenses,
        'monthly_total': monthly_total,
        'categories_summary': categories_summary,
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
