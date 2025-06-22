from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExpenseForm
from .utils import get_dashboard_context, get_expense_list_context


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
    Vista refactorizada - limpia y profesional
    Maneja tanto peticiones normales como HTMX usando funciones auxiliares
    """
    # Obtener todo el contexto usando las funciones auxiliares
    context = get_expense_list_context(request.user, request.GET)
    
    # ¿Es una petición HTMX? Devolver solo contenido parcial
    if request.headers.get('HX-Request'):
        return render(request, 'expenses/partials/expense_list_content.html', context)
    
    # Petición normal: devolver página completa
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



